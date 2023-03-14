---
layout: default
title: Baklava TestNet
nav_order: 5
---

# Baklava TestNet

https://user-images.githubusercontent.com/41792982/224991015-a96e570e-0213-4e09-b563-77cafb5797b1.mp4


<br>
<br>

Baklava TestNet is a test network for developers. You can use this network to testng and distributing your applications. After the [registiration](https://naruno.org/baklava-testnet/) you will get 1002 coins. You can use this coins for creating a one more user (1000) and sending 100 transaction (2). Also you can use you coins without creating an one more user (Multiple devices that used one account).

## Wallet Creation
In the mails that we will send you must to give an wallet and for this you should use our [Wallet Creating](https://docs.naruno.org/getting-started/usages.html#wallet-creating) document. And please your wallet that used for baklava testnet via `narunocli --wallet wallet_id` command.

You can check your coins via this api:

http://test_net.1.naruno.org:8000/balance/get/?address=your_wallet_address

{: .highlight }
Dont forget to moving your backups to an safe location. You can use `narunocli --narunoexport` command for creating and finding your backups

### Wallet Import
If you have an zip file for your backup you can use:
```console
narunocli --narunoimport zip_file_localtion
```

## Switching to Baklava TestNet
The Naruno designed for working in connected and participated network. But we add a setting for using baklava testnet. You can use this setting via `narunocli --baklavaon` command. After this command you can use baklava testnet.


## Using

After switching you can use our 4 lines web3 integration system.

### Installing API Requirements

```console
pip3 install naruno-api
```

### Starting in a command line interface

```console
narunoapi
```

### Creating Web3_App.py

Please use this code for creating a Web3 application in 4 lines.

```python
from naruno.apps.remote_app import Integration

integration = Integration("Your_App_Name", password="Your_Wallet_Password", host="localhost")

integration.send("Your_Action_Name", "Your_Data", "Recipient_Address")

print(integration.get())
```

