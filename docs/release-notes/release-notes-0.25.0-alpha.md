---
title: 0.25.0-alpha
parent: Release Notes
nav_order: 51
---

# 0.25.0-alpha Release Notes

With this minor release we maded many improvements for transaction checking system.
Also we added docs for dowloading and using builds and we made some improvements 
in the GitHub.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Transactions
Added limit and type checkers to transaction checking system.

## Documentation
Added docs for dowload and using builds.

## GitHub
We added environments and removed after workflow run Tests trigger. 
Also we made some changes for on push and pull_requests triggers.


# 0.25.0-alpha change log

### Transactions
* transaction: Amount and fee decimal amount limited to block.transaction_fee by @onuratakan in https://github.com/Naruno/Naruno/pull/579
* transaction: Set limits for fromUser and toUser and added type checking for transaction elements by @onuratakan in https://github.com/Naruno/Naruno/pull/589
* transaction: Limit set for len of data by @onuratakan in https://github.com/Naruno/Naruno/pull/591
### Documentation
* docs: Added new dowload links and using docs by @onuratakan in https://github.com/Naruno/Naruno/pull/583
* docs: Added document for application developer that closing the thread after succeed works by @onuratakan in https://github.com/Naruno/Naruno/pull/585
### GitHub
* github: Changed Deploy environment name to Deploys by @onuratakan in https://github.com/Naruno/Naruno/pull/574
* github: Added Builds environment by @onuratakan in https://github.com/Naruno/Naruno/pull/575
* github: Added Tests environment by @onuratakan in https://github.com/Naruno/Naruno/pull/577
* github: Removed after workflow run Tests triggers by @onuratakan in https://github.com/Naruno/Naruno/pull/582

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
