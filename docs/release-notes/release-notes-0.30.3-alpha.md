---
title: 0.30.3-alpha
parent: Release Notes
nav_order: 62
---

# 0.30.3-alpha Release Notes

With this path we added new APIs about transactions. and added some fix and improvements.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## API
Added new APIs for getting the transactions about wallets. Like sended, received, validated and not validated.

## GitHub
Seperated environments for codecov, unit, functional and stability tests.

# 0.30.3-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Transactions
* api: Added new /transactions/ based APIs that seperated by sended or received and validated or not validated by @onuratakan in https://github.com/Naruno/Naruno/pull/1148
* api: Added `/transactions/all` API for getting all transactions by @onuratakan in https://github.com/Naruno/Naruno/pull/1154
* api: Removed some useless parts of new `/transactions/` APIs by @onuratakan in https://github.com/Naruno/Naruno/pull/1156
### Docs
* docs: Fixed 0.30.1 full changelog link by @onuratakan in https://github.com/Naruno/Naruno/pull/1151
* docs: Added new API docs by @onuratakan in https://github.com/Naruno/Naruno/pull/1155
### GitHub
* github: Changed environments by @onuratakan in https://github.com/Naruno/Naruno/pull/1149


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.30.2-alpha...v0.30.3-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
