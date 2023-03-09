---
title: Usages
parent: Getting Started
nav_order: 3
---

# Usages

## Wallet Creating

Wallet creation is the first step to start using the Naruno blockchain. For this you can use your all type installations but for now we will give introduction for cli with pip installation.

```python
pip install naruno
```

After installation you can create wallet with this command

```python
narunocli --createwallet password
```

and lastly you can see your wallet via:

{: .highlight }
Please dont use first wallet its not encrypted because its used for node communication signatures. When you create a new wallet like above its start from second wallet

```python
narunocli --printwallet
```

{: .warning }
Please save you backups via results of `narunocli --narunoexport` command.

## Building a Test Network

Test network creation A way to build a fully-fledged and functional naruno blockchain network with automatic and manual options.You can develop applications on this network or do all other blockchain activities.
So you should start with this

- [Building a Test Network](https://docs.naruno.org/building_a_test_network/)

## User Interfaces

The project has a user-friendly interface that allows you to access and manage different features and functions. Here is a link to the documentation on the user interface:
İt is recommended to try the user interfaces

- [User Interfaces](https://docs.naruno.org/concepts/user_interfaces.html)

## Creating a APP

Our project provides a variety of tools and resources for creating applications. Here is a link to the documentation on how to create applications using the project:
Experience the power of Naruno with fast and efficient applications

- [Creating a APP](https://docs.naruno.org/creating_a_app/)
