---
title: Transactions
parent: Systems
nav_order: 2
---

Transactions are the mainstay of every operation on the network. If the transaction is correct, it will be accepted.
Pseudo transactions are not accepted and will not propagated through the network.

The core elements of an [transaction](https://github.com/Decentra-Network/Decentra-Network/blob/master/src/transactions/transaction.py#L13) are:
* A number from the account class that ensures that 
each transaction is valid once.
* A signature proving that the sender approved the transaction.
* Sender's public key.
* Receiver's address.
* A text that can be written into the transaction.
* A int or float amount to be sent.
* Fee for transaction.
* time: Sending time.


## Dynamic Transaction Fee System
Transaction fees are determined by a special [mechanism](https://github.com/Decentra-Network/Decentra-Network/blob/master/src/blockchain/block/block_main.py#L292), and must be charged at a fee that the majority of the network can accept, sometimes the network may not accept the standard transaction fee.

* Each node sets an optimum transaction amount for itself
* Currently default optimum transaction amount 10 ([Pull Request #66](https://github.com/Decentra-Network/Decentra-Network/commit/82e124919e8031fed1a784bf5ddb023febb8a587#diff-17332442b68875a6b66bd4989c8ed80c22ce1c836445aa7042145b0c0627cf30R62))

***

## Sending a Transaction
The sending transaction is done by the send.py and send function. 
send function is verry simple, it takes the password, receiver address, amount and data.

```python
from transactions.send import send

password = "123"

to_user = "ex_wallet"

amount = 5000

send(password, to_user, amount, data=None):
```
