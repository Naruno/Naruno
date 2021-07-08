# Using the Docker Test
You must pull images and tag must be decentra-network-api

## Install From Github Packages
`docker pull ghcr.io/decentra-network/api:latest`

`docker image tag ghcr.io/decentra-network/api decentra-network-api`

## Running Auto Test | [![Open in Cloud Shell](https://img.shields.io/badge/Open-Google%20Cloud%20Shell%20Tutorial-blue)](https://ssh.cloud.google.com/cloudshell/open?cloudshell_git_repo=https://github.com/Decentra-Network/Decentra-Network&cloudshell_tutorial=doc/systems/test_environments/google_cloud_shell/docker_auto_tests_tutorial.md)

`python3 test_decentra_network_docker.py`

## Start the Network Only
`python3 docker.py -nn 3`

-nn = node number

# Using the Local Test

## Install From Github
`git clone https://github.com/Decentra-Network/Decentra-Network`

`cp -r Decentra-Network 2`

`cp -r Decentra-Network 3`
.
.
.

You run the decentra-network nodes as this types:
## Preparing The Nodes
* Each node will be in different dir
Node Number 3
1.node Run api with 8000 port
2.node Run api with 8010 port
3.node Run api with 8020 port
.
.
.

## Running Auto Test
`python3 test_decentra_network_local.py`

## Start the Network Only
`python3 local.py -nn 3`

-nn = node number
