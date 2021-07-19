---
title: Using
parent: Getting Started
nav_order: 2
---

# Opening

## Normal
### GUI Mode
`python3 src/gui.py`

### CLI With Menu
`python3 src/cli.py -m`

### CLI With Parameters
Please visit https://decentra-network.github.io/Decentra-Network/systems/cli.html for cli arguments.
`python3 src/cli.py -h`

### API
Please visit https://decentra-network.github.io/Decentra-Network/systems/api.html for api referance.
`python3 src/api.py`


## Docker
### Run CLI Menu
`docker run -v decentra-network-cli:/Decentra-Network/src/db/ --network=host -it ghcr.io/decentra-network/cli /bin/sh`
Now you can access the Decentra Network CLI in bash.

### Run API
`docker run -v decentra-network-api:/Decentra-Network/src/db/ --network=host -dit ghcr.io/decentra-network/api`
Now Decentra Network Core broadcasts on port 8000 in API mode.

# Using Steps
- Create at least 3 node (differend directory/image)
- Create wallets
- Open the Debug mode
- Select a node and open the test mode
- Get ids of nodes and add every other node as unl node
- Start the node servers
- Connect all nodes together
- Get block on the node with test mode on

The network is started and working, now you can send transaction.
