---
layout: default
title: Embedded
parent: Creating a APP
nav_order: 2
---

# Creating a Embedded APP

If you want to develop applications inside Decentra network you can use our Apps Engine. The Apps engine gives you new data and you can send data with Naruno send functions. With this you can easily integrate your today Applications with Blockchain on Decentra network.

## Prerequisites

- A Network (You can check the [Building a Test Network](https://docs.naruno.net/building_a_test_network/) for this)

## First Stage: Generating the Sceleton

The embedded applications must have a communication section that written in python. And this files must be in some rules.

- Naruno
  - decentra_network
    - apps
      - App_Name
        - App_Name_main.py

_If you use a test network you can change the "Naruno" folder with your test network node folders ex. "Naruno-0"._

In this files you should write a function that catch the new datas of your application. Naruno will send the new data to this function but you must check and organize your data.

When a transaction is confirmed, the function here is triggered.

```python
// App_Name_main.py

import sys

def app_name_send_tx(action, app_data, password, to_user):
  return

def app_name_main_tx(tx):
  sys.exit()
```

\*You must use sys.exit() in your `app_name_main_tx` function to exit the app when you are done. Because the applications are running on a Thread.

## Second Stage: Sending the Data

You can send a data for your appplication with send function, you can import this function from Naruno.

```python
from decentra_network.transactions.send import send
```

Before the sending you must determine the data, for this first you must create a dictionary and determine a action for your data. The action is a string, we are use this for processing the data in getting function.

```python
data = {
  "action": "app_name_action_name",
  "app_data": "data"
}
```

After that you can send the data with send function. The send function has 3 parameters.

- The first parameter is the password of wallet, you can be able to get from installation.

- Second parameter is to_user, with this parameter you can choose the user that you want to send the data. Example in a messaging app you can send the data to message recipient. This parameter should be a string that equal 40 characters.

And the last parameter is the data, you can pass the data that you created before.

```python
send(
  "123", # Password
  "Naruno-00000000000000000000002",
  data=data,
)
```

And in the final we must combine the send system to App_Name_main.py file. You must use the `app_name_send_tx` function for this. And now we are settings from your applications.

```python
// App_Name_main.py

import sys

from decentra_network.transactions.send import send

def app_name_send_tx(action, app_data, password, to_user) -> bool:
  data = {
    "action": action,
    "app_data": app_data
  }

  result = send(
    password,
    to_user,
    data=data,
  )

  return result # True or False

def app_name_main_tx(tx):
  sys.exit()

```

## Third Stage: Getting the Data

When you send the data, the data will be available in the to_user. You can get the data in to_user with `app_name_main_tx` function.

Firtly we must check the action of data. If the action is equal to the action that we determined before, we can process the data.

In this examples if the action is equal to "app_name_action_name" we will print the data.

Firstly we will import the `wallet_import_all` from `decentra_network.wallet.wallet_import` for checking transactions came us or not.
And we will import `get_logger` from `decentra_network.lib.log` of Naruno for printing.

```python
from decentra_network.wallet.wallet_import import wallet_import_all
from decentra_network.lib.log import get_logger

```

After we will import json

```python
import json
```

Now we are ready for function:

```python



def app_name_main_tx(tx):
  app_name_logger = get_logger("app_name")
  if tx.toUser in wallet_import_all(3):
    tx = tx.data.replace("'", '"')
    tx = json.loads(tx)
    if tx["action"] == "app_name_action_name":
        app_name_logger.info(tx["app_data"])
  sys.exit()
```

## Final

```python
// App_Name_main.py

import json
import sys

from decentra_network.transactions.send import send
from decentra_network.wallet.wallet_import import wallet_import_all
from decentra_network.lib.log import get_logger


def app_name_send_tx(action, app_data, password, to_user) -> bool:
  combined_data = {
    "action": action,
    "app_data": app_data
  }

  result = send(
    password,
    to_user,
    data=combined_data,
  )

  return result # True or False

def app_name_main_tx(tx):
  app_name_logger = get_logger("app_name")
  if tx.toUser in wallet_import_all(3):
    tx = tx.data.replace("'", '"')
    tx = json.loads(tx)
    if tx["action"] == "app_name_action_name":
        app_name_logger.info(tx["app_data"])
  sys.exit()



```

## Expectations

With this app, you can send a public message to a user that you dont know his/her ip address and not using a server.

You can use this app for safe and private messaging but if you want more, you should sending the datas far from Naruno (We have best methods for transactions but this situation is same for all blockchains) and after a while you should save the datas in Naruno. This is a good way for mostly of the applications.

Example of a message sending:

The first user is sending a message to the second user.

```python
from decentra_network.apps.app_name.app_name_main import app_name_send_tx

app_name_send_tx(
  "app_name_action_name", # Action
  "Hello World", # Data
  "123", # Password
  "Naruno-00000000000000000000002", # To User
)
```

The second user device is getting the message and print the data to `app_name.log` that be found at

- Naruno
  - decentra_network
    - logs
      - app_name.log

```log
// app_name.log
2022-09-07 18:03:02,399 - app_name - INFO - Hello World
```

## Next Steps

You should save the datas for using in a frontend or backend service, for this you can use this type for your `app_name_main_tx` function.

Firstly you should import the pickle library.

```python
import pickle
```

```python

def get_list():
  try:
    with open("app_name_action_name.pickle", "rb") as f:
      return pickle.load(f)
  except:
    return []

def add_to_list(data):
  old = get_list()
  old.append(data)
  with open("app_name_action_name.pickle", "wb") as f:
    pickle.dump(old, f)

def app_name_main_tx(tx):
  app_name_logger = get_logger("app_name")
  if tx.toUser in wallet_import_all(3):
    tx = tx.data.replace("'", '"')
    tx = json.loads(tx)
    if tx["action"] == "app_name_action_name":
        app_name_logger.info(tx["app_data"])
        add_to_list(tx)
  sys.exit()
```

Now you can access all datas from the `get_list` function.

```python
from decentra_network.apps.app_name.app_name_main import get_list

print(get_list())
```
