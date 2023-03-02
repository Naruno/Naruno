---
title: 0.2.0-alpha
parent: Release Notes
nav_order: 2
---

# 0.2.0-alpha Release Notes

In this minor version, the feature of using multiple wallets has been added.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Using Multiple Wallets

Now you can go to the wallet option from the GUI-Wallets panel
and type w in the CLI and select the wallet you want to use.

- The first wallet will be used in your relationship with the network. You can choose a wallet for all other transactions.

  # 0.2.0-alpha change log

### Settings

- A "wallet" variable added to settings that specifies and stores the wallet used

### Wallet

- Removed some unnecessary dprint
- Changed the Wallet_Import() function, added the use default wallet situation, for this use -1 (Wallet_Import(-1,0))

### CLI

- Added the wallet menu and function
- Changed the Wallet_Import() function to get default wallet
- Added a small loading animation
- Removed the address printing in get balance (gb)

### Blockchain

- Changed the Wallet_Import() function to get default wallet

### GUI

- Added the wallet button BottomSheet and function
- Added auto balance reflesher for switching to the new wallet
- Changed the Wallet_Import() function to get default wallet
- Added the float filter to send coin
- Solved the send coin minumum amount control

### Send Coin

- Changed the Wallet_Import() function to get default wallet

### Requirements.txt

- Added the version info of the modules.

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
