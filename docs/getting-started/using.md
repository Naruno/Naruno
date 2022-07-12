---
title: Using
parent: Getting Started
nav_order: 2
---

# Opening

## Normal

### GUI Mode

`python3 decentra_network/gui.py`

### CLI With Menu

`python3 decentra_network/cli.py -m`

### CLI With Parameters

`python3 decentra_network/cli.py -h`

### API

`python3 decentra_network/api.py`

## Pip

### GUI Mode

`dngui`

### CLI With Menu

`dncli -m`

### CLI With Parameters

`dncli -h`

### API

`dnapi`

## Docker

### Run CLI Menu

`docker run -v decentra-network-cli:/app/Decentra-Network/decentra_network/db/ --network=host -it ghcr.io/decentra-network/cli /bin/sh`

Now you can access the Decentra Network CLI in bash.

### Run API

`docker run -v decentra-network-api:/app/Decentra-Network/decentra_network/db/ --network=host -dit ghcr.io/decentra-network/api`

Now Decentra Network Core broadcasts on port 8000 in API mode.

## Builds

You should use `chmod +x filename` to make the file executable in linux.

### GUI Mode (Win32)

`./Decentra-Network-GUI.exe`

### CLI With Menu (Win32)

`./Decentra-Network-CLI.exe -m`

### CLI With Menu (Linux)

`./Decentra-Network-CLI -m`

### CLI With Parameters (Win32)

`./Decentra-Network-CLI.exe -h`

### CLI With Parameters (Linux)

`./Decentra-Network-CLI -h`

### API (Win32)

`./Decentra-Network-API.exe`

### API (Linux)

`./Decentra-Network-API`

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

# Using as a library

Please look at function referances, you can find in [referances](https://decentra-network.github.io/Decentra-Network/getting-started/using.html#referances).

# Referances

- [CLI Arguments](https://decentra-network.github.io/Decentra-Network/systems/cli.html)
- [API Referance](https://decentra-network.github.io/Decentra-Network/systems/api.html)
- [Function Referances](https://decentra-network.github.io/Decentra-Network/systems/functions.html)
