---
title: 0.20.0-alpha
parent: Release Notes
nav_order: 43
---

# 0.20.0-alpha Release Notes

With this minor release we fix many problems about block system, time amd transactions.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

### Block

Block time optimizer removed and block time increased to 10 seconds.

### Transactions

Disabled multi transaction from the same account in the same block.

# 0.20.0-alpha change log

### Block

- block: Block time change smoothed by @onuratakan in https://github.com/Naruno/Naruno/pull/441
- block: Block time increased by @onuratakan in https://github.com/Naruno/Naruno/pull/445
- block: Block time optimizer removed

### Transactions

- transactions: Disabled multiple transactions from the same account in one block by @onuratakan in https://github.com/Naruno/Naruno/pull/444

### Tests

- tests: Removed a functional test because its useless

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
