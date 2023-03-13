---
layout: default
title: Baklava TestNet
nav_order: 5
has_children: true
---

# Baklava TestNet

Baklava TestNet is a test network for developers. You can use this network to testng and distrbuting your applications. After the [registiration](https://naruno.org/baklava-testnet/) you will get 1002 coins. You can use this coins for creating a one more user (1000) and sending 100 transaction (2). Also you can use you coins without creating an one more user (Multiple devices that used one account).

In the mails that we will send you must to give an wallet and for this you should use our [Wallet Creating](https://docs.naruno.org/getting-started/usages.html#wallet-creating) document. And please your wallet that used for baklava testnet via `narunocli --wallet wallet_id` command.

You can check your coins via this api:

http://test_net.1.naruno.org:8000/balance/get/?address=your_wallet_address

{: .highlight }
Dont forget to moving your backups to an safe location. You can use `narunocli --narunoexport` command for creating and finding your backups

{: .warning }
Please use this command for opening baklava testnet mod `narunocli --baklavaon`.

And after plase use our [Using](https://docs.naruno.org/baklava-testnet/using.html) document for creating an Web3 application in 4 lines.
