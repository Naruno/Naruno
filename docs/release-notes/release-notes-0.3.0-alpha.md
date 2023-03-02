---
title: 0.3.0-alpha
parent: Release Notes
nav_order: 3
---

# 0.3.0-alpha Release Notes

With this minor version, some bugs and mistakes have been
resolved and password feature has been added to wallets.
Wallets are now protected with the password you set.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Wallet Encryption

You can now set a separate password for each wallet,
which you will need to enter when creating a wallet
or when a privatekey is required.

- The first wallet cannot be encrypted as it is used for your connection to the network in the background, but you will still be prompted for a password.

  # 0.3.0-alpha change log

### Git Ignore

- Added the \*.blockshash

### Save block to blockchain db

- Added the blocks hash saving

### CLI

- Added some functionality to retrieve password securely for send coin and wallet create.
- Removed useless calculations

### GUI

- Added some field to retrieve password securely for send coin and wallet create

### Encryption (NEW)

- Added the encrypt and decrypt by password function

### Send

- Added the password element to function

### Send Coin

- Added the password element to function

### Wallet

- Added the password element to wallet create and wallet import function
- Added the password controller
- Added encrypt based saving system
- Added decrypt based get privatekey system

### Node test

- Password addition for wallet creation

### Wallet test

- Password addition for wallet creation and importing the wallet (privatekey)

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- @cpyberry
