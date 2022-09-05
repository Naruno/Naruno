---
layout: default
title: Embedded
parent: Creating a APP
nav_order: 1
---


# Creating a Embedded APP

If you want to develop applications inside Decentra network you can use our Apps Engine. The Apps engine gives you new data and you can send data with Decentra Network send functions. With this you can easily integrate your today Applications with Blockchain on Decentra network.

## Prerequisites
- A Network (You can check the [Building Test Network](https://docs.decentranetwork.org/building_test_network/))


## First Stage: Generating the Sceleton

The embedded applications must have a communication section that written in python. And this files must be in some rules.
- Decentra-Network
  - decentra_network
    - apps
      - App_Name
        - App_Name_main.py



In this files you should write a function that catch the new datas of your application. Decentra Network will send the new data to this function but you must check and organize your data.

When a transaction is confirmed, the function here is triggered.

```python
// App_Name_main.py

def app_name_send_tx(action, data):
  return    

def app_name_main_tx(data):
  return    
```

*You must use sys.exit() to exit the app when you are done. Because the applications are running on a Thread.

