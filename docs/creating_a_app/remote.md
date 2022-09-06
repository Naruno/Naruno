---
layout: default
title: Remote
parent: Creating a APP
nav_order: 1
---


# Creating a Remote APP

If you want to develop applications outside of Decentra network you can use [APIs](https://docs.decentranetwork.org/referances/apis.html). The APIs gives you new data and you can send data with Decentra Network send functions. With this you can easily integrate your today Applications with Blockchain on Decentra network.

## Prerequisites
- A Network (You can check the [Building Test Network](https://docs.decentranetwork.org/building_test_network/) for this)
- Running API (You can check the [Starting the API](https://docs.decentranetwork.org/referances/apis.html#starting-the-api) for this)


## First Stage: Generating the Sceleton

The remote application that we will create in the next sections should be have a integrastion system. For this we will use 


- decentra_network_integration.py


In this file we have a two class function, the first one is send we will use for sending data, and the second one is get we will trigger this in some time and we will get the new data from the network.

```python
// decentra_network_integration.py

class Integration:

  def send(action, app_data, password, to_user):
    return    

  def get():
    return
```


## Second Stage: Sending the Data

Firtly we are importing the requests library for sending the data to the API.

```python
import requests
```

Before the sending you must determine the data, for this first you must create a dictionary and determine a action for your data. The action is a string, we are use this for processing the data in getting function.

```python
data = {
  "action": "app_name_action_name",
  "data": "data"
}
```

After that you can send the data with `/send` API. The API has 3 post parameters. 

- The first parameter is the password of wallet, you can be able to get from installation.

- Second parameter is to_user, with this parameter you can choose the user that you want to send the data. Example in a messaging app you can send the data to message recipient. This parameter should be a string that equal 40 characters.

And the last parameter is the data, you can pass the data that you created before.
```python
request_body = {
  "password": "123",
  "to_user": "Decentra-Network-00000000000000000000002",
  "data": data,  
}
```
  
And now we are send this via `requests.post`

```python
response = requests.post('http://0.0.0.0:8000/send', data=request_body)
```

After the request you can check the response with `response.text`. If the response is not equal to "false" the data is sent successfully.

After this command if the result is not equal to "false" the sent successfully.

*You should check the API port.*



And in the end of this section we can combine this operations at `decentra_network_integration.py` with `Integration.send` function.


```python
// decentra_network_integration.py

import requests

class Integration:

  def send(action, app_data, password, to_user) -> bool:
    data = {
      "action": action,
      "data": app_data
    }

    request_body = {
      "password": password,
      "to_user": to_user,
      "data": data,  
    }

    response = requests.post('http://0.0.0.0:8000/send', data=request_body)

    return True if response.text != "false" else False


  def get():
    return

```

Now you can use `Integration.send` functions as you want.

Ex. Sending a message

```python
from decentra_network_integration import Integration

Integration.send(
  action="app_name_action_name",
  app_data="Hello World",
  password="123",
  to_user="Decentra-Network-00000000000000000000002"
)
```

## Third Stage: Getting the Data

When you send the data, the data will be available in the to_user. You can get the manualy with `	/export/transactions/json` API.

When we get the transactions we should find news for apps. For this we will prepare a cache mechanism, every time we get the transactions we will remove the old transactions from the cache and add the new transactions to the cache.


After we get the new datas, firstly we must check the action of data. If the action is equal to the action that we determined before, we can process the data.

In this examples if the action is equal to "app_name_action_name" we will print the data.

```python	

class Integration:
  cache = []

  def get():

    response = requests.get('http://0.0.0.0:8000/export/transactions/json')
    transactions = response.json()

    for transaction in transactions:
      if transaction in Integration.cache:
        transactions.remove(transaction)
      else:
        Integration.cache.append(transaction)

    for transaction in transactions:
      if transaction["data"]["action"] == "app_name_action_name":
        print(transaction["data"])
```



And the final is
  
```python
// decentra_network_integration.py

  import requests

  class Integration:
    cache = []

    def send(action, app_data, password, to_user) -> bool:
      data = {
        "action": action,
        "data": app_data
      }

      request_body = {
        "password": password,
        "to_user": to_user,
        "data": data,  
      }

      response = requests.post('http://0.0.0.0:8000/send', data=request_body)

      return True if response.text != "false" else False




    def get():

      response = requests.get('http://0.0.0.0:8000/export/transactions/json')
      transactions = response.json()

      for transaction in transactions:
        if transaction in Integration.cache:
          transactions.remove(transaction)
        else:
          Integration.cache.append(transaction)
      for transaction in transactions:
        if transaction["data"]["action"] == "app_name_action_name":
          print(transaction["data"])
```

## Expectations

With this app, you can send a public message to a user that you dont know his/her ip address and not using a server. 

You can use this app for safe and private messaging but if you want more, you should sending the datas far from Decentra Network (We have best methods for transactions but this situation is same for all blockchains) and after a while you should save the datas in Decentra Network. This is a good way for mostly of the applications.

Example of a message sending:

The first user is sending a message to the second user.

```python
from decentra_network_integration import Integration

Integration.send(
  action="app_name_action_name",
  app_data="Hello World",
  password="123",
  to_user="Decentra-Network-00000000000000000000002"
)
```

The second user device is ready to getting the message and print the data. Fot this we will use `Integration.get` function in a loop for getting new datas every 3 seconds.



```python
import time

from decentra_network_integration import Integration

while True:
  Integration.get()
  time.sleep(3)
```

```bash
> Hello World
```
