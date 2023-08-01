---
layout: default
title: Introduction
parent: Baklava TestNet
nav_order: 1
---

# Baklava TestNet

Baklava TestNet is a test network for developers. You can use this network to testng and distributing your applications. After the [registiration](https://naruno.org/baklava-testnet/) you will get 1002 coins. You can use this coins for creating a one more user (1000) and sending 100 transaction (2). Also you can use you coins without creating an one more user (Multiple devices that used one account).

## Upgrading

- Please save your backup via `narunocli --narunoexport`. You should move a safe place The file that given after the command. If any problem you can use this file for restoring your naruno via `narunocli --narunoimport your_zip_file`.

```console
pip3 install naruno --upgrade
```

## Preparing

The Naruno designed for working in connected and participated network. But we add a setting for using baklava testnet. You can use this setting via this command:

```console
narunocli --baklavaon
```

You can check your coins via this command:

```console
narunocli --getbalance
```

{: .highlight }

> If your balance is smaller from 0 you should check your other wallets. For viewing other wallets you should use `narunocli --printwallet` and after you should switch to other wallet via `narunocli --wallet your_wallet_id_from_printwallet`

After switching you can use our 4 lines web3 integration system.

## Using
- [Creating a Remote App for Naruno](https://docs.naruno.org/creating_a_app/remote.html)
- [Ovenden Incentive](https://docs.naruno.org/baklava-testnet/ovenden-incentive.html)