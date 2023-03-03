---
title: 0.12.0-alpha
parent: Release Notes
nav_order: 29
---

# 0.12.0-alpha Release Notes

This minor release includes new features and some improvements.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Added Licence to Setup Files

The MPL-2.0 licence added to cli, api and gui setup files.

## Fix For Hash Calculation

With this minor release the part of account list saving fixed.

## Backup and Restore Function For Accounts and Block Hash

With this release if the account list and block temp files is
in the db the new blockchain started with this block information
and accounts list.

## Code Quality Improvements

Some functions are moved to another places and added docstrings
to some functions.

## Fix For Auto Builers

The first step of autoh builers using with command line parameters
changed to delete.

## Security Circle Feature For Auto Builders

With this feature the networks that maded with different and multiple
security circle can build.

## Spec Files For Windows

Added spec files for EXE file creation for windows.

# 0.12.0-alpha change log

### Spec Files

- Added spec files for cli
- Added spec files for api
- Added spec files for gui

### Auto Builders

- Changed the first in parameter usage to deletion
- Increased the sleep after the installation.
- Added parameter as number_of_security_circle to Naruno_Docker class
- Added parameter as number_of_security_circle to Naruno_Local class
- Added parameter to command line parameter of docker base auto builers
- Added parameter to command line parameter of local base auto builers
- Added network creation that seperated to security circle

### Setups

- Added MPL-2.0 licence to cli setup
- Added MPL-2.0 licence to api setup
- Added MPL-2.0 licence to gui setup

### Accounts

- GetAccounts function moved to accounts/get_accounts.py
- Added docstring to GetAccounts function
- GetAccounts_part function moved to accounts/get_accounts_part.py
- Added docstring to GetAccounts_part function

### Block

- Added a parameter to Block class as previous_hash and default is "0"
- Removed SaveBlockshash_part function from creation
- Removed save_accounts_part function from creation
- Added a control point for account list restoring

### Create Block

- Added a control point for block hash restoring

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
