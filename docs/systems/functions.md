---
title: Functions
parent: Systems
nav_order: 5
---

# Function Referances

| Subject       | Import Command                            | Uses                                          |
| ------------- | ----------------------------------------- | --------------------------------------------- |
| Import Wallet | `from wallet.wallet import Wallet_Import` | `Wallet_Import(account,mode,password = None)` |

| Send Transaction | `from transactions.send import send` | `send(password, to_user, amount=None, data=None)` |
| Get Transaction History | `from transactions.get_my_transaction import GetMyTransaction` | `GetMyTransaction()` |
