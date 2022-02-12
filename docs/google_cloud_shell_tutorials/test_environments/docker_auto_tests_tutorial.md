---
layout: default
title: 404
nav_exclude: true
---

# Docker Test Environments Tutorial

## Download API Docker

```bash
docker pull ghcr.io/decentra-network/api:latest
```

## Building Test Environment with Auto Builders
With auto builders, you can build your test environment in a automated way.

It's takes 60 seconds.

```bash
python3 auto_builders/docker.py -nn 3 -scn 1 -i -r -s
```
<walkthrough-footnote>Docker Test Environments Tutorial</walkthrough-footnote>

## Conclusion

Now you can use our [API referance](https://docs.decentranetwork.org/systems/api.html#api-referance) to send transactions to your test environment.

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>



<walkthrough-footnote>Docker Test Environments Tutorial</walkthrough-footnote>
