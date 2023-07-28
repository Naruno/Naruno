---
title: 0.60.0-alpha
parent: Release Notes
nav_order: 138
---

# 0.60.0-alpha Release Notes

This release include KOT transformation and stability improvements.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility
Old backups are just compatible with wallet section. Other sections are not compatible with old backups.

# Notable changes

## KOT Transformation
Every database system moved to KOT. This change will make the system more stable and faster.

## Stability Improvements
The system has been made stable for high load.


# 0.60.0-alpha change log
<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Wallet
* wallet: Moved wallet save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1677
### Accounts
* accounts: Moved commander save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1671
* accounts: Moved account save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1682
### Apps
* apps: Moved cache save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1679
### Blockchain
* blockchain: Moved blockshash save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1681
* blockchain: Moving block save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1683
### Transactions
* transactions: Moved my transaction save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1672
* transactions: Moved pending transaction save&get to by @onuratakan in https://github.com/Naruno/Naruno/pull/1673
* transactions: Added syncing feature for tx validation for baklava network users by @onuratakan in https://github.com/Naruno/Naruno/pull/1690
### Node
* node: Moved unl save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1675
* node: Moved connected node save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1676
### API
* tests: Moving test api perpetual time tester function save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1678
### GUI
* gui: Added baklava setting by @onuratakan in https://github.com/Naruno/Naruno/pull/1685
* gui: Changed box layout to grid layout for popups by @onuratakan in https://github.com/Naruno/Naruno/pull/1689
* gui: Fixed signature copy of get my transaction section by @onuratakan in https://github.com/Naruno/Naruno/pull/1691
* gui: Fixed amount situations and data info on send by @onuratakan in https://github.com/Naruno/Naruno/pull/1692
### Lib
* lib: Added KOT database code by @onuratakan in https://github.com/Naruno/Naruno/pull/1656
* lib: Moved settings save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1670
* lib: Moved config save&get to KOT by @onuratakan in https://github.com/Naruno/Naruno/pull/1674


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.59.0-alpha...v0.60.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
