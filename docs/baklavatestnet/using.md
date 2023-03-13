---
layout: default
title: Creating Web3 App
parent: Baklava TestNet
nav_order: 1
---

# Starting API

## Installing API Requirements
```console
pip3 install naruno-api
```
## Starting in a command line interface
```console
narunoapi
```

# Creating Web3_App.py

Please use this code for creating a Web3 application in 4 lines.

```python
from naruno.apps.remote_app import Integration

integration = Integration("Your_App_Name", password="Your_Wallet_Password", host="localhost")

integration.send("Your_Action_Name", "Your_Data", "Recipient_Address")

print(integration.get())
```