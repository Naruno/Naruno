---
title: 0.46.0-alpha
parent: Release Notes
nav_order: 89
---

# 0.46.0-alpha Release Notes

This minor release includes a number of changes across different categories. In the Accounts category, support has been added for getting balance from baklava testnet. The CLI category has been updated to fix an issue with the `getbalanc`e function. The Docs category has seen several changes, including typo fixes in the baklava testnet document and removal of the `pip install` and wallet creation sections from that document, as well as the addition of an upgrading section.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Accounts
The accounts category has been updated to include support for getting balance from baklava testnet, thanks to @onuratakan in their pull request at https://github.com/Naruno/Naruno/pull/1490.

## CLI
In the CLI category, the `getbalance` function has been fixed to correctly print its result, thanks to @onuratakan's pull request at https://github.com/Naruno/Naruno/pull/1491.

## Docs
Several changes have been made in the Docs category. Typos have been fixed in the baklava testnet document, thanks to @onuratakan's pull request at https://github.com/Naruno/Naruno/pull/1489. The `pip install` section has been removed from the wallet creation doc, as per @onuratakan's pull request at https://github.com/Naruno/Naruno/pull/1492. An upgrading section has been added to the baklava testnet document, thanks to @onuratakan's pull request at https://github.com/Naruno/Naruno/pull/1493. Lastly, the wallet creation section has been removed from the baklava testnet document, as per @onuratakan's pull request at https://github.com/Naruno/Naruno/pull/1494.


# 0.46.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Accounts
* accounts: Added support for getting balance from baklava testnet by @onuratakan in https://github.com/Naruno/Naruno/pull/1490
### CLI
* cli: Fixed getbalance function printing result by @onuratakan in https://github.com/Naruno/Naruno/pull/1491
### Docs
* docs: Fixed some typos for baklava testnet document by @onuratakan in https://github.com/Naruno/Naruno/pull/1489
* docs: Removed pip install section from wallet creation doc by @onuratakan in https://github.com/Naruno/Naruno/pull/1492
* docs: Added upgrading section to baklava testnet document by @onuratakan in https://github.com/Naruno/Naruno/pull/1493
* docs: Removed wallet creation section from baklava testnet by @onuratakan in https://github.com/Naruno/Naruno/pull/1494


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.45.1-alpha...v0.46.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
