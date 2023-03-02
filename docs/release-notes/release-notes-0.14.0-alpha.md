---
title: 0.14.0-alpha
parent: Release Notes
nav_order: 31
---

# 0.14.0-alpha Release Notes

This minor release includes new features and many improvements.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Added `data` Variable to Send Transaction Functions

With this feature, you can send transactions with `data` variable.

## CreateTransaction Function Improvements

The CreateTransaction function is divided and formatted into two functions as follows: SendTransactiontoTheBlock and CheckTransaction.

## send_the_coin Function Improvements

The send_the_coin is merged into the send function.

## Code Quality Improvements

The all files under `src/consensus` and some files
under `src/blockchain` have been linted and code
style has been improved.

## New Unit Test

Added a unit test for the flask.

## More Stable Functional Tests

As a result of the studies carried out to reduce
possible errors in the tests, the functional tests
were made more stable.

# 0.14.0-alpha change log

### Unit Test

- Added a unit test for the flask as test_api.py

### Accounts

- Changed the parameter order of the `get_balance` function

### Wallet

- Reordered the parameters of the `get_balance` function

### Transaction

- Changed the parameters of the `TXAlreadyGot` function to transaction objects
- Removed some unnecessary calculation for transaction check
- Removed `Transaction.get_hash` function
- Transaction.time changed to transaction.transaction_time
- Removed the `send_the_coin` function
- Removed public and private key pramater from the `send` function
- Changed the parameter order of the `send` function
- `send_the_coin` function codes moved into the `send` function
- Removed the `CreateTransaction` function and added `SendTransactiontoTheBlock`
  and `CheckTransaction` functions

### CLI

- Added scd function to CLI menu for sending coin with data

### API

- Added a API point as `/send/coin-data/<address>/<amount>/<data>/<password>` to send coin with data

### Functional Tests

- Added double check for all tests

### Docs

- Added new send-data API point to API reference
- Added API port information to API docs
- Sending transaction docs is changed

### Google Cloud Shell Tutorials

- Functional test based cloud shell tutorials changed to auto builders
- Tutorials have been improved

### Block

- Made code quality improvements
- Removed some unused imports

### Consensus

- Made code quality improvements

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
