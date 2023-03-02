---
title: 0.30.0-alpha
parent: Release Notes
nav_order: 59
---

# 0.30.0-alpha Release Notes

With this minor release we improve the performance and update the block time and some of parts of our system changed to sqlite3. Also we are maded some other improvements.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
Changed saving method of blockshash and blockshash_part to sqlite3 and changed block time to 22 second.

## Transactions
Added a new layer for checking transactions.

## API
Deprecated `/send_old/coin` API and added a logger for errors.

## Packages
Added a new packages for testing and remote app.

## Docs
Some docs fixed for true usages.

## Tests
Added timer tests for performance.

## Lib
Fixed perpetual timer structure and added performance analyzers.


# 0.30.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Accounts
* accounts: Added multiple account saving in one time ability by @onuratakan in https://github.com/Naruno/Naruno/pull/1111
### Blockchain
* blockchain: Changed json based save system of blockshash list to sqllite by @onuratakan in https://github.com/Naruno/Naruno/pull/1115
* blockchain: Changed blockshash_part saving method with sqllite3 by @onuratakan in https://github.com/Naruno/Naruno/pull/1118
* blockchain: Increased block time by @onuratakan in https://github.com/Naruno/Naruno/pull/1120
### Transactions
* transactions: Improved checking len system with checking maximum amount and transaction fee by @onuratakan in https://github.com/Naruno/Naruno/pull/1096
* transactions: Changed checking logs for if not situations by @onuratakan in https://github.com/Naruno/Naruno/pull/1097
### API
* api: Deprecated /send_old/coin api by @onuratakan in https://github.com/Naruno/Naruno/pull/1091
* api: Added error logging by @onuratakan in https://github.com/Naruno/Naruno/pull/1108
### Packages
* packages: Added test requirements  by @onuratakan in https://github.com/Naruno/Naruno/pull/1105
* packages: Added remote app requirements by @onuratakan in https://github.com/Naruno/Naruno/pull/1107
* packages: Added naruno_remote_app by @onuratakan in https://github.com/Naruno/Naruno/pull/1126
* packages: Added naruno_tests package by @onuratakan in https://github.com/Naruno/Naruno/pull/1127
* packages: Changed author email by @onuratakan in https://github.com/Naruno/Naruno/pull/1128
* packages: Changed url by @onuratakan in https://github.com/Naruno/Naruno/pull/1129
### Docs
* docs: Changed `python` to `python3` by @onuratakan in https://github.com/Naruno/Naruno/pull/1090
* docs: Changed `/send` to `/send/` by @onuratakan in https://github.com/Naruno/Naruno/pull/1100
### Tests
* tests: Set heartbeat get and save time to less than 9 by @onuratakan in https://github.com/Naruno/Naruno/pull/1121
### Lib
* lib: Some improvements for perpetualTimer by @onuratakan in https://github.com/Naruno/Naruno/pull/1103
* lib: Added performance analyzers by time by @onuratakan in https://github.com/Naruno/Naruno/pull/1112



**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.29.1-alpha...v0.30.0-alpha


# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
