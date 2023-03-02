---
title: 0.19.0-alpha
parent: Release Notes
nav_order: 42
---

# 0.19.0-alpha Release Notes

With this minor release we have added many new features and improved the correction of the system.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

### Wallet

Added a transform proccess for address function in the wallet system.

### Auto-Builders

Added different .out files for different nodes in local auto builder.

### Transactions

Changed order mechanism for transactions and accounts for stability and correction.

### CLI - GUI

Removed unused library in CLI and GUI.

### Setups

Synced the required libraries between requirements/api.txt and setups.

# 0.19.0-alpha change log

### Wallet

- wallet: Added a transform process to Address function by @onuratakan in https://github.com/Naruno/Naruno/pull/437

### Auto-Builders

- auto_builders: Local based .out file set differently for each node by @onuratakan in https://github.com/Naruno/Naruno/pull/428

### Transactions

- transactions: Changed the order mechanism by @onuratakan in https://github.com/Naruno/Naruno/pull/431
- transaction: Added a new list to proccess the transaction function for sacalability in big lists by @onuratakan in https://github.com/Naruno/Naruno/pull/439

### CLI - GUI

- Removed loguru library by @onuratakan in https://github.com/Naruno/Naruno/pull/434

### Setups

- setups: Synced the requirements with api setup.py by @onuratakan in https://github.com/Naruno/Naruno/pull/429

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
