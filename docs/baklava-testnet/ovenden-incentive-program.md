---
layout: default
title: Ovenden Incentive Program
parent: Baklava TestNet
nav_order: 2
---

# Ovenden Incentive Program

In Baklava we are introduce an incentive for testing our official applications and after all the Integration library. You can get your incentive with this document.

## Requirements
- You should have an registered baklava user. If you dont have you can register via [this link](https://naruno.org/baklava-testnet/).


## Application: Web3 App | NEW

### What is Web3 App?
[Web3 App](https://github.com/Naruno/Web3_App) is an platform for everyone in the Baklava TestNet. In Web3 you can send a message with 100 character limit and you can select a username with 15 character limit. 

Your posts is will be in in this [address](http://web3.test_net.1.naruno.org:2000/)

*Submission of inappropriate content will be penalized

### Installation
You can install APS via this command:
```console
pip3 install Web3_App
```

### Setting Password
Enter you wallet pass with this command.
```console
web3 --host "0.0.0.0" --port 4444 set_pass <password>
```

### Setting Username
Please select an username with this command (Max 15 Character and its should be unique)
```console
web3 --host "0.0.0.0" --port 4444 username <username>
```

### Sending a Post
You can send one post in every day not more its will be incentvized (Max 100 Character)

```console
web3 --host "0.0.0.0" --port 4444 post <content>
```


*Then wait for 5 minutes.


{: .highlight }

> If you get the `True` message you will get your incentive. Don't sent twice time because everyone can get only one incentive.

{: .highlight }

> If you can get the `True` message and you are an registered baklava user and you didnt send multiple time just close application with `Ctrl+C` and try again after 5 minutes.


### Vew Posts
You can see your and others posts in [here](http://web3.test_net.1.naruno.org:2000/)


### Controlling Your Incentive
We will set your incentives as global in all networks. But the loads are take time. We will notificate on [Discord](https://discord.gg/Vpn2tfEEWc). After loading you can check your incentive via this command:

```console
narunocli --getbalance
```