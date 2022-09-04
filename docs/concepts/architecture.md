---
layout: default
title: Architecture
parent: Concepts
nav_order: 5
has_children: False
---

# The Architecture

The Decentra Network is a decentralized network of nodes that run the Decentra Network software. The Decentra Network software is a different implementation for blockchain.

We are use three layers of the Decentra Network architecture:

- Layer 1: Far from the concepts
  - We have a frontends and backend in this layer, the fronends are the CLI, API, and GUI. The backend is the circulation system.
- Layer 2: Connection to the concepts
  - b
- Layer 3: Using the concepts
  - c



```Mermaid
flowchart LR
DN[Decentra Network]

subgraph FRONTEND
  CLI
  API
  GUI
end



subgraph BACKEND
  Circulation
end




subgraph Layer_1
  direction LR
  FRONTEND
  BACKEND
end


subgraph Layer_2
  Transfer
end

Transfer[Transfer System]






CONSENSUS[Consensus System]
ACCOUNT[Account System]
TRANSACTION[Transaction System]
BLOCKCHAIN[Blockchain System]
APPS[Apps System]
NODE[Node System]
WALLETS[WALLET System]

subgraph Layer_3
    direction LR
    CONSENSUS
    ACCOUNT
    TRANSACTION
    BLOCKCHAIN
    APPS
    NODE
    WALLETS
end

DN --> Layer_1
Layer_1 --> Layer_2
Layer_2 --> Layer_3




```
