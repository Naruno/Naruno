---
title: 0.11.0-alpha
parent: Release Notes
nav_order: 25
---

# 0.11.0-alpha Release Notes

This minor release includes many improvements and some addition.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Code Queality Improvements

Docstring has been added to the codes, some useless functions have been removed,
and finally some functions have been separated.

## Main Package Added to GUI and API Package as a Requirement

With this patch, users who install the naruno_gui and naruno_api
packages will also install the naruno package.

# 0.11.0-alpha change log

### Notice

Please control the name of moved and deleted functions.

### Setups

- Added the naruno==0.11.0 to naruno_gui as a requirement.
- Added the naruno==0.11.0 to naruno_api as a requirement.

### send_coin

- This function is moved to send the coin function inside.

### send_the_coin

- Parameter name chaned (to_user, coin_amount, password).

### Block Main

- Removed the sequance number parameter.

### Save Accounts && Save Accounts Part

- This functions moved to src/accounts/save_accounts.py and src/accounts/save_accounts_part.py

### send_my_response_on_transaction

- Removed this function.

### change_transaction_fee

- This function moved to src/transactions/change_transaction_fee.py

### createTrans

- This function moved to src/transactions/create_transaction.py

### PropagatingtheTX

- This function moved to src/transactions/propagating_the_tx.py

### TXAlreadyGot

- This function moved to src/transactions/tx_already_got.py

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- @cpyberry
- Bahri Can ERGÜL
- Taha Kutay ALPTEKİN
