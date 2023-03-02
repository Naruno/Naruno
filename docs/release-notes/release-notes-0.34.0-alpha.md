---
title: 0.34.0-alpha
parent: Release Notes
nav_order: 69
---

# 0.34.0-alpha Release Notes

With this minor release we added a ordering mechanism for pending to validating function that add important to transactions that have a higher fee.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Transactions
We added a function called `OrderbyFee` and this function is used in `PendingtoValidating` function. This function orders the transactions by fee and return.

# 0.34.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Transactions
* transactions: Added a ordering by transaction fee mechanism to pending to validating by @onuratakan in https://github.com/Naruno/Naruno/pull/1209


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.33.0-alpha...v0.34.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
