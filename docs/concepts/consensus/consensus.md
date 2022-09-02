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


## Federated Byzantine Agreement (FBA)
The Federated Byzantine Agreement goal is reach success with no centralization trend, no safety risk (Preventing sybil attacks) and fast speed. FBA got power from it's participant method. For the success on this theory, our FBA implementation is use two stages, the first stage is the Pre-Consensus (Round 1), and the second stage is the Consensus (Round 2). And we use Heart to  run this two stages.

# Decentra Network Consensus Circulation System
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

```mermaid
flowchart RL
    subgraph Consensus Mechanism Circulatory System
        subgraph Heart
            direction TB

            perpetualTimer[perpetualTimer]
            heartbeat[2 Beat in a second]
            consensus_trigger[consensus_trigger]


            perpetualTimer --- heartbeat
            heartbeat --> consensus_trigger
        end

        %% add in-line style
        Heart:::someclass
        classDef someclass fill:#5ec295;


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
```