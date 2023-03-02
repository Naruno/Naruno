---
title: 0.35.2-alpha
parent: Release Notes
nav_order: 72
---

# 0.35.2-alpha Release Notes

With this path we improved the performance of GetBalance function.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Accounts
In this path we remove the checking given account Address and account same time from the db. We add a argument "dont_convert" for GetBalance function if its true we dont convert the given account to Address, otherwise we convert the given account to Address and return the balance.

# 0.35.2-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Accounts
* accounts: Removed looking address and original argument balance together, added a argument for dont generate address for balance control of to account by @onuratakan in https://github.com/Naruno/Naruno/pull/1226


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.35.1-alpha...v0.35.2-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
