---
title: Proofs
parent: Concepts
nav_order: 5
---

# The Proofs

Naruno have a system and mindset for proof. If you sende a transaction to the network, the network must be process your request and finish the consensus. But there is a important thing, the block and other materials to calculate hash of the block just saved from sender (you) and receiver. Others does not save your data, just process.

But what happen if i want to get proof of my data (transaction in other word) For this we have a system with saving from sender (you) and receiver system. This is parting system. With this your node (sender) and receiver node will be saved the block and other materials to calculate part of blockshash with this items the other nodes that not saved yours block and materials can be able to check your proof.

When you send a transaction to the network your node will be add to current block.

```mermaid
flowchart LR
    TX[TX 1] -->|Send TX| B1[Block 1]
```

And after adding your node will be waiting for complating part_amount that include block that your transaction added to.

```mermaid
flowchart LR
    BLH[Blocks Hash Part Complated that include Block 1]
    BLH --> Proof
    subgraph Proof[Proof of TX 1]
        block[Block 1]
        blockshash[Block Hash]
        blockshashpart[Block Hash Part]
        accounts[Accounts]
    end

```

With this operation you have a proof and now you can share any node this proof and they can check easily.

```mermaid
flowchart LR
    OtherNode[Other Node]
    OtherNode --> proof
    OtherNode -->AnyBlock
    proof[Proof of TX 1]
    proof --> check
    AnyBlock[Any Block]
    AnyBlock --> check

    check{Check Proof}
    check --> True
    check --> False
```
