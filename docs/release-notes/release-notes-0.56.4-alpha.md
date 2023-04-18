---
title: 0.56.4-alpha
parent: Release Notes
nav_order: 127
---

# 0.56.4-alpha Release Notes

We are pleased to announce the path of version v0.56.4-alpha of Naruno. This update includes enhancements and bug fixes in Apps, Transactions, and Lib.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
The latest update for Naruno introduces a new feature where the API can now be initialized for stopped parallel apps. This was made possible through the contribution of @onuratakan (pull request #1585). In addition to this, a fault tolerance system for raw data has also been added, which can help prevent data loss. This was also contributed by @onuratakan (pull request #1588).

## Transactions
With the latest Naruno update, a fault tolerance system has been added to prevent issues with broken transaction files. This can help ensure the integrity of your transaction data. This new feature was contributed by @onuratakan (pull request #1586).

## Lib
A syntax error with the JSON in the status transactions of us element has been fixed with the latest Naruno update. This issue was resolved thanks to the contribution of @onuratakan (pull request #1587).

# 0.56.4-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Added initialize the API for stopped paralel Apps by @onuratakan in https://github.com/Naruno/Naruno/pull/1585
* apps: Added fault tolerance for raw datas by @onuratakan in https://github.com/Naruno/Naruno/pull/1588
### Transactions
* transactions: Added faut tolerance for broken my transacton files by @onuratakan in https://github.com/Naruno/Naruno/pull/1586
### Lib
* lib: Fixed json syntax error in status transactions_of_us element by @onuratakan in https://github.com/Naruno/Naruno/pull/1587


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.56.3-alpha...v0.56.4-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
