# Docker Test Environments Tutorial

## Pulling
First we need to download our docker image.

```bash
docker pull ghcr.io/decentra-network/api:latest
```

## Name Changing
Second we will make its name available for use.

```bash
docker image tag ghcr.io/decentra-network/api decentra-network-api
```

## Running The Auto Tests
Finaly we run our automated test tool, it sets up and tests the network for us.

```bash
python3 test_environments/docker/test_decentra_network_docker.py
```

## Conclusion

Done!
