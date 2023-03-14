---
title: 0.45.0-alpha
parent: Release Notes
nav_order: 87
---

# 0.45.0-alpha Release Notes

This release includes a number of new features, improvements, and bug fixes across various categories such as Apps, Blockchain, CLI, API, Packages, Docs, and Lib. Notably, multiple account support has been added to the Apps category, and new APIs have been added to retrieve sequence numbers and user balances. Additionally, some documentation links have been fixed, and new documents have been added. This release also welcomes new contributors to the project.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
The latest update to the Naruno app now supports multiple accounts, thanks to a contribution from @onuratakan. You can find more details about this update in pull request #1484.

## Blockchain
The Naruno blockchain now includes support for the Baklava testnet, thanks again to @onuratakan's contribution in pull request #1480. Additionally, the accounts list hash calculation has been fixed, which can be seen in pull request #1482.

## CLI
The Naruno CLI has received an update that allows for changing publisher mode via both menu and arguments, thanks to @onuratakan's contribution in pull request #1471.

## API
There are two new additions to the Naruno API. The first is an API that allows for retrieving the sequence number of a specific user, which was contributed by @onuratakan and can be seen in pull request #1477. The second is an API for getting an user's balance, which was also contributed by @onuratakan and can be found in pull request #1478.

## Packages
The author_email field in the Naruno package has been changed, thanks to @onuratakan's contribution in pull request #1466.

## Docs
Several documentation updates have been made to the Naruno project. The image links have been fixed, thanks to a contribution from @whodaff in pull request #1472. A new document on creating a wallet has been added to the usages section, thanks to @onuratakan's contribution in pull request #1479. Typos in both the building testnetwork manual and the introducing section have been corrected, thanks to contributions from @sergiomateiko and @omahs, respectively, in pull requests #1481 and #1483.

## Lib
The Naruno library now includes publisher mode setting and backward support for settings, thanks to contributions from @onuratakan in pull requests #1469 and #1485.

# 0.45.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Added multiple account support by @onuratakan in https://github.com/Naruno/Naruno/pull/1484
### Blockchain
* blockchain: Added baklava testnet users by @onuratakan in https://github.com/Naruno/Naruno/pull/1480
* blockchain: Fixed accounts list hash calculation by @onuratakan in https://github.com/Naruno/Naruno/pull/1482
### CLI
* cli: Added publisher mode changer to menu and arguments by @onuratakan in https://github.com/Naruno/Naruno/pull/1471
### API
* api: Added a api for gettng sequance number of specific user by @onuratakan in https://github.com/Naruno/Naruno/pull/1477
* api: Added get balance of an user by @onuratakan in https://github.com/Naruno/Naruno/pull/1478
### Packages
* packages: Changed the author_email by @onuratakan in https://github.com/Naruno/Naruno/pull/1466
### Docs
* docs: Fixed image links by @whodaff in https://github.com/Naruno/Naruno/pull/1472
* docs: Added wallet creating document in usages by @onuratakan in https://github.com/Naruno/Naruno/pull/1479
* docs: Fixed buiding testnetwork manuel typo by @sergiomateiko in https://github.com/Naruno/Naruno/pull/1481
* docs: Fixed introducing typos by @omahs in https://github.com/Naruno/Naruno/pull/1483
### Lib
* lib: Added publisher mode setting by @onuratakan in https://github.com/Naruno/Naruno/pull/1469
* lib: Added backward support for settings by @onuratakan in https://github.com/Naruno/Naruno/pull/1485

## New Contributors
* @whodaff made their first contribution in https://github.com/Naruno/Naruno/pull/1472
* @sergiomateiko made their first contribution in https://github.com/Naruno/Naruno/pull/1481

**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.44.4-alpha...v0.45.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- @omahs
- @sergiomateiko
- @whodaff
