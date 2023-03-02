---
title: 0.4.3-alpha
parent: Release Notes
nav_order: 9
---

# 0.4.3-alpha Release Notes

This patch includes a important optimization and fix.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Added The New Optimized Calculating The Hash System

We apply merkle root to list elements with a maximum
of 100000 using the partitioning system we recommend
at this address:
https://github.com/Naruno/Naruno/issues/141

This gives us super practicability and speed.

### Two Transactions From The Same User in One Block Bug Fixed

When the same person made two transactions in one block,
a bug was triggered and the whole system was crashing.
With this patch, this critical bug has been closed.

# 0.4.3-alpha change log

### Gitignore

- Added the new part file

### Account

- Added the new function for part file saving and getting
- Added the **str** function for "Two Transactions From The Same User in One Block Bug"

### Block

- Added the part file create code

### Blocks Hash

- Added the new function for part file saving and getting
- Some fixes for if not exist situation

### Calculate Hash

- Added the new optimized calculating the hash system for blocks hash
- Added the new optimized calculating the hash system for accounts

### Save Block to Blockchain DB

- Added the saving function for part file

### Process The Transaction

- Removed some unused codes
- Added some code for "Two Transactions From The Same User in One Block Bug"

### Readme

- Changed the version number to "0.4.3-alpha"

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
