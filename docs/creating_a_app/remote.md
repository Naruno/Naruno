---
layout: default
title: Remote
parent: Creating a APP
nav_order: 1
---
Creating a Remote App for Decentra Network
==========================================

If you're interested in developing applications on Decentra Network that can interact with external systems, you can use the Decentra Network API. The API provides access to data on the blockchain and enables you to send data to the network via the network's send function. By using the API, you can easily integrate your existing applications with Decentra Network.

Prerequisites
-------------

To use the Decentra Network API, you'll need the following:

*   A running network (see [Building a Test Network](https://docs.decentranetwork.net/building_a_test_network/) for instructions on how to set this up)
*   A running API (see [Starting the API](https://docs.decentranetwork.net/referances/apis.html#starting-the-api) for instructions on how to set this up)

### Installing the Decentra Network Remote App library

To get started with the Decentra Network Remote App, you'll need to install the `decentra_network` and `decentra-network-remote-app` libraries. You can do this by running the following command:

```bash
pip3 install decentra_network decentra-network-remote-app
```

Overview
--------

The Decentra Network Remote App library provides a simple way to integrate your applications with the Decentra Network blockchain. You can use this library to send data to and receive data from the network, allowing you to create decentralized applications that leverage the security and immutability of the blockchain.

The library provides two basic functions for interacting with the network:

1.  Send: Use the `Integration.send()` function to send data to a specific user on the network. The data will be signed with your public key and stored on the blockchain.
    
2.  Get: Use the `Integration.get()` function to retrieve data from the network. Your node will retrieve the data from the blockchain and return it to your application.
    

Integration
-----------

Using the Decentra Network Remote App library, you can easily send and receive public messages between users on the network. Here's how to get started:

### Sending a Message

To send a message to a user on the network, use the `Integration.send()` function. The function takes three parameters: an action, application data, and the address of the user you want to send the message to. Here's an example:

```python
from decentra_network.apps.remote_app import Integration

integration = Integration("app_name")

integration.send("action", "app_data", "to_user")
```

### Receiving a Message

To receive a message from the network, use the `Integration.get()` function. This function retrieves the data from the network and returns it to your application. Here's an example:

```python
from decentra_network.apps.remote_app import Integration
import time

integration = Integration("app_name")

while True:
  print(integration.get())
  time.sleep(3)
```

This code will retrieve data from the network every three seconds and print it to the console.

### Caching

The Decentra Network Remote App library has an active caching system to provide a real network experience. The system caches retrieved data to avoid returning the same data multiple times. However, you can reset or disable the cache using the `integration.delete_cache()` and `integration.disable_cache()` functions.