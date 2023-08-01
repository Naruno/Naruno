---
title: 0.60.2-alpha
parent: Release Notes
nav_order: 140
---

# 0.60.2-alpha Release Notes

This path fix some bugs and add some abilities.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility
Old backups are just compatible with wallet section. Other sections are not compatible with old backups.

# Notable changes

## Apps
In this path we fix the bugs and we add some control parameters for multiple sendings. And we made some value adjustments for more stable integration.

## Transactions
In this path we add a reset ability for my transactions db when the db is changed from outside.

## Node
In this path we add last_control mechanism and dedicated variables to self_candidates for fixing a bug.

## API
In this path we fix /balance/get/ and /sequence/get/ endpoint block gathering ways.


# 0.60.2-alpha change log


<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Some time adjustment made for more stable Integration by @onuratakan in https://github.com/Naruno/Naruno/pull/1701
* apps: Some value adjustment made for more stable Integration by @onuratakan in https://github.com/Naruno/Naruno/pull/1702
* apps: Fixed send_splitter resend bug by @onuratakan in https://github.com/Naruno/Naruno/pull/1704
* apps: Added a parameter to Integration for setting multiple sending wait amount between sends by @onuratakan in https://github.com/Naruno/Naruno/pull/1705
### Transactions
* transactions: Added a reset ability for my transactions db when the db is changed from outside by @onuratakan in https://github.com/Naruno/Naruno/pull/1700
### Node
* node: Added last_control mechanism and dedicated variables to self_candidates for fixing a bug by @onuratakan in https://github.com/Naruno/Naruno/pull/1698
### API
* api: Fixed /balance/get/ and /sequence/get/ endpoint block gathering ways by @onuratakan in https://github.com/Naruno/Naruno/pull/1703
### Docs
* docs: Fixed Google Analytics tracking code by @onuratakan in https://github.com/Naruno/Naruno/pull/1699
### Lib
* lib: Updated KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1697


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.60.1-alpha...v0.60.2-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
