---
layout: default
title: Consensus
parent: Concepts
nav_order: 4
has_children: False
---

# The Consensus

Consensus is an aggrement method, if a mission on the multiple computer system needs an agreement on the same data, the consensus is the method to achieve this goal.

Blockchain is have a distributed concept, which means the data is stored on multiple computers, and the consensus is the method to achieve the agreement on the data. There is a many consensus methods, the first one is the Proof of Work. It's reach the success with hard working on the computer, think if someone wants a reward from you, you should check and control his works and if it enough you should give him the reward. This is the same as the Proof of Work, the computer that has the most work should get the reward, and the reward is from the new block. And new block is the new data that will be added to the blockchain.

The Proof of Work is a amazing start for Blockchain technology, but it's not the best method, because it's need a lot of energy and time to reach the consensus. The Proof of Work is the first method that reach the consensus, but it's not the best method, and there is a lot of other methods that can reach the consensus with less energy and time. We use the best method, The Federated Byzantine Agreement, is our consensus method.


# Consensus Circulation System
## Heart
The Heart is most important part, it's run the stages after a decision.

Heart beat in two times in a second and runs the 'decentra_network.consensus.consensus_main.consensus_trigger' functions

### consensus_trigger
Consensus trigger is a starter by checking the block status if block is ready to be added to the blockchain (validated), it will add the block to the blockchain and start the finished processes. If the block is not ready, it will start consensus processes.


#### finished_main
Finished main is a function that will run after the block is validated. It will check the block status for resetting if if its suitable (Have an transaction) the finished_main will save the block and run apps and transaction saver other wise function that not do these just saves and calls PendingtoValidating.
#### ongoing_main
This function is run for ongoing consensus process. 

- If block.round_1 is False it will run the consensus_round_1 function.
- If block.round_1 is True and block.round_2 is False its start consensus_round_2.

And return the block.


# Consensus Ongoin System | Federated Byzantine Agreement (FBA)
The Federated Byzantine Agreement goal is reach success with no centralization trend, no safety risk (Preventing sybil attacks) and fast speed. FBA got his power from it's participant method. For the success on this theory, our FBA implementation that on the ongoing_main is use two stages, the first stage is the Round 1, and the second stage is Round 2.

## Round 1
The first stage of consensus will sync the transaction that selected as True from majority. For this every node send self candidate block that include suggested transactions.

When a node got enough candidate block (80% of UNL Nodes) the proccessing is starts and transaction process and the transaction that selected from majority will be added to the block. After the transaction process is done, the new block is created and ready to round 2.

### Comunication
```mermaid
sequenceDiagram
    participant Node_A
    participant Node_B
    participant Node_C
    
            
    Node_A->>+Node_B: transaction_a and transaction_b should be in Block 15
    Node_A->>+Node_C: transaction_a and transaction_b should be in Block 15

    Node_B->>+Node_A: transaction_b should be in Block 15
    Node_B->>+Node_C: transaction_b should be in Block 15

    Node_C->>+Node_A: transaction_b should be in Block 15
    Node_C->>+Node_B: transaction_b should be in Block 15
```

### Decision
```mermaid
classDiagram
    Node_0_validating_list_not_validated --|> Node_B
    Node_0_validating_list_not_validated --|> Node_C
    Node_0_validating_list_not_validated: +transaction_a
    Node_0_validating_list_not_validated: +transaction_b

    Node_0_validating_list_validated <|-- Node_B
    Node_0_validating_list_validated <|-- Node_C
    Node_0_validating_list_validated: +transaction_b

    class Node_B{
      +transaction_B
    }
    class Node_C{
      +transaction_B
    }
```	

## Round 2
The last stage of consensus is the round 2, in this stage the block hash that created in the round 1 will be validated by the nodes. The nodes send self block hash to UNL nodes. When the block got enough validation result (80% same of UNL Nodes) the block will be added to the blockchain as a validated block.

### Comunication
```mermaid
sequenceDiagram
    participant Node_A
    participant Node_B
    participant Node_C
    
            
    Node_A->>+Node_B: The new block hash is 321
    Node_A->>+Node_C: The new block hash is 321

    Node_B->>+Node_A: The new block hash is 123
    Node_B->>+Node_C: The new block hash is 123

    Node_C->>+Node_A: The new block hash is 123
    Node_C->>+Node_B: The new block hash is 123
```

### Decision
```mermaid
classDiagram
    Node_0_block_not_validated --|> Node_B
    Node_0_block_not_validated --|> Node_C
    Node_0_block_not_validated: HASH 321

    Node_0_block_validated <|-- Node_B
    Node_0_block_validated <|-- Node_C
    Node_0_block_validated: HASH 123

    class Node_B{
      HASH 123
    }
    class Node_C{
      HASH 123
    }
```	


## Consensus Diagram

```mermaid
flowchart RL
    subgraph Circulation
        subgraph Heart
            direction TB

            perpetualTimer[perpetualTimer]
            heartbeat[2 Beat in a second]
            consensus_trigger[consensus_trigger]


            perpetualTimer --- heartbeat
            heartbeat --> consensus_trigger
        end



        subgraph consensus_trigger
            direction TB

            validated{block.validated}
            finished_main[[finished_main]]
            ongoing_main[ongoing_main]

            return[return block]

            validated -- True --> finished_main
            validated -- False --> ongoing_main

            finished_main --o return

            ongoing_main --o return


        end

        subgraph finished_main
            direction TB

            true_time{true_time}


            returntrue[return True]
            returnfalse[return False]

            PendingtoValidating[PendingtoValidating]
            SaveBlock[SaveBlock]

            true_time -- True --> block.reset_the_block
            true_time -- False --o returnfalse

            block.reset_the_block -- True --o AppsTrigger --- transactions_main --- SaveBlockshash --- SaveBlockstoBlockchainDB --o PendingtoValidating --- SaveBlock
                            
            block.reset_the_block -- False --o PendingtoValidating --- SaveBlock


            SaveBlock --o returntrue


        end

        subgraph ongoing_main
            direction TB

            block.round_1{block.round_1}

            block.round_2{block.round_2} 

            returnBlock[return Block]

            block.round_1 -- True --> block.round_2
            block.round_2 -- True --> returnBlock
            block.round_2 -- False --> consensus_round_2
            block.round_1 -- False --> consensus_round_1

            consensus_round_1 --o returnBlock
            consensus_round_2 --o returnBlock

        end    
    end

    subgraph consensus_round_1
        direction TB

        round_checkconsensus_round_1{round_check}
        returnTrueconsensus_round_1[return True]
        returnFalseconsensus_round_1[return False]

        round_checkconsensus_round_1 -- True --> round_processconsensus_round_1 --o returnTrueconsensus_round_1
        round_checkconsensus_round_1 -- False --> send_my_block --o returnFalseconsensus_round_1

    end   

    subgraph consensus_round_2
        direction TB

        round_checkconsensus_round_2{round_check}
        returnTrueconsensus_round_2[return True]
        returnFalseconsensus_round_2[return False]

        round_checkconsensus_round_2 -- True --> round_processconsensus_round_2 --o returnTrueconsensus_round_2
        round_checkconsensus_round_2 -- False --> send_my_block_hash --o returnFalseconsensus_round_2

    end   
```