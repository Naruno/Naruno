---
title: 0.4.4-alpha
parent: Release Notes
nav_order: 10
---

# 0.4.4-alpha Release Notes

This patch includes the some fixes for Accounts hash calculations.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Decentra-Network/Decentra-Network/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Fixes for Accounts Hash Calculations

Added some missing data, and added some fields to track changes
and now Naruno Core provide a more stable accounts hash calculation.

# 0.4.4-alpha change log

### Block

- Added a element for edited account tracking

### Calulate Hash

- The part controller operator is changed
- Added the edited account adding to the account hash calculation
- Added the clear for after the edited account adding

### Proccess The Transaction

- Added the edited account saving to a element for edited account tracking

### Readme

- Changed the version number to "0.4.4-alpha"

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
