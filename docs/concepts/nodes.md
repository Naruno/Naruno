---
title: Node
parent: Concepts
nav_order: 9
---

# The Node

Node are the hard working concepts of Naruno, every data is sending and getting via Node. The nodes are have a checking process before connections. This is ip, port and ID. If the node that try to connect have an similar node and port settings Node is not accept this requests. Also we have a mechanism for checking the IDs named as Unique Node List UNL.

## Unique Node List (UNL)

This is a unique trusted node lists for every node. If you want to add a node to your node you must be added it's ID to UNL list. Otherwise your node will not accept the node that you want to add.

## Security Circle

Security circle is an important concept for Naruno. This is a circle that consisting of nodes. When a group node example Node 1, Node 2 and Node 3 trusted each other they are be security circle. This is a circle that can be used for sending and getting datas to each other and process the consensus.

```mermaid
flowchart LR
Node_1(((Node 1)))
Node_2(((Node 2)))
Node_3(((Node 3)))

Node_1 <--> Node_2
Node_2 <--> Node_3
Node_3 <--> Node_1

subgraph SC1[Security Circle 1]
    Node_1
    Node_2
    Node_3
end



Node_4(((Node 4)))
Node_5(((Node 5)))
Node_6(((Node 6)))

Node_4 <--> Node_5
Node_5 <--> Node_6
Node_6 <--> Node_4

subgraph SC2[Security Circle 2]

    Node_4
    Node_5
    Node_6
end

Node_7(((Node 7)))
Node_8(((Node 8)))
Node_9(((Node 9)))

Node_7 <--> Node_8
Node_8 <--> Node_9
Node_9 <--> Node_7

subgraph SC3[Security Circle 3]
    Node_7
    Node_8
    Node_9
end


subgraph Naruno
    direction LR
    SC1
    SC2
    SC3
end

Node_1 <--> Node_9
Node_3 <--> Node_4
Node_6 <--> Node_7

```

## Syncing

When you want to syncing from an node in Naruno, the node will include your node to sync wait list. When the Gap blocks are camed the node will send the block to your node. This syncing is very fast because the blocks are verry small and you just need last block.
