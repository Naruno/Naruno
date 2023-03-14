---
layout: default
title: Baklava TestNet
nav_order: 5
---

# Baklava TestNet

Baklava TestNet is a test network for developers. You can use this network to testng and distributing your applications. After the [registiration](https://naruno.org/baklava-testnet/) you will get 1002 coins. You can use this coins for creating a one more user (1000) and sending 100 transaction (2). Also you can use you coins without creating an one more user (Multiple devices that used one account).

## Upgrading

For new versions and backward support you should get a backup first.

```console
narunocli --narunoexport
```

Its gives a zip file location and please move or copy this file to an safe place.

Now we will upgrade the our software:

```console
pip3 uninstall naruno -y
```

```console
pip3 install naruno --no-cache
```

And now we will use our backup

```console
narunocli --narunoimport your_zip_file
```

## Wallet Creation

{: .warning }

> Skip if you have already registered and received your coins

- Firstly if you have a backup you should pass this section with using importing command (`narunocli --narunoimport zip_file_localtion`).

In the mails that we will send you must to give an wallet and for this you should use our [Wallet Creating](https://docs.naruno.org/getting-started/usages.html#wallet-creating) document. And please switch your wallet that you created for baklava testnet via this command:

```console
narunocli --wallet wallet_id
```

You can check your coins via this command:

```console
narunocli --getbalance
```

Dont forget to moving your backups to an safe location. You can use `narunocli --narunoexport` command for creating and finding your backups

## Using

The Naruno designed for working in connected and participated network. But we add a setting for using baklava testnet. You can use this setting via this command:

```console
narunocli --baklavaon
```

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
