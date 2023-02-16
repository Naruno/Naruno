---
layout: default
title: Remote
parent: Creating a APP
nav_order: 1
---

# Creating a Remote APP

If you want to develop applications outside of Decentra network you can use [APIs](https://docs.decentranetwork.net/referances/apis.html). The APIs gives you new data and you can send data with Decentra Network send functions. With this you can easily integrate your today Applications with Blockchain on Decentra network.

## Prerequisites

- A Network (You can check the [Building a Test Network](https://docs.decentranetwork.net/building_a_test_network/) for this)
- Running API (You can check the [Starting the API](https://docs.decentranetwork.net/referances/apis.html#starting-the-api) for this)

### Installing requirements

```bash
pip3 install decentra_network decentra-network-remote-app
```

## Idea

The remote app integration system idea is creating a super simple way to creating a usability on blockchain for todays applications. And with this way you can easily integrate your applications with blockchain via two basic steps.

### Step 1: Send

We developed a simple way to send data to a user. You can send a data to a user with address. The data will be signed with the your public key and will be sent to the blockchain.

### Step 2: Get

The second step is getting the data. You can get the data with your active node. Your node will catch the data.

## Integration

With this app, you can send a public message to a user that you dont know his/her ip address and not using a server.

You can use this app for safe and private messaging but if you want more, you should sending the datas far from Decentra Network (We have best methods for transactions but this situation is same for all blockchains) and after a while you should save the datas in Decentra Network. This is a good way for mostly of the applications.

### Send

The first user is sending a message to the second user.

```python
from decentra_network.apps.remote_app import Integration

integration = Integration("app_name")

integration.send("action", "app_data", "touser")

integration.get()
```

### Get

The second user device is ready to getting the message and print the data. Fot this we will use `Integration.get` function in a loop for getting new datas every 3 seconds.

```python
from decentra_network.apps.remote_app import Integration
import time

integration = Integration("app_name")

while True:
  print(integration.get())
  time.sleep(3)
```

```bash
> Hello World
```

#### Caching

We have an active and default system in the get step. The system is caching the datas for generating a real network experience. If there is a new data the system will return the new data. But after in another new call of 'integration.get()' the system wouldnt return the old data.

But you can reset the cache or disable it with `integration.delete_cache()` and `integration.disable_cache()` functions.
