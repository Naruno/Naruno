---
title: 0.51.0-alpha
parent: Release Notes
nav_order: 101
---

# 0.51.0-alpha Release Notes

The release notes for version v0.51.0-alpha of Naruno are now available. This update includes various changes and improvements to the apps, auto-builders, blockchain, transactions, node, packages, and lib categories. The changes include added fault tolerance for big data in apps, reduced time sleep after installation in auto-builders, increased max transaction number and added a setting for disabling block saving in blockchain, fixed self-posting transactions in transactions, added bypass exception for deleting buffer of data for enough data size situations in node, bumped werkzeug version in packages, and added a method to get the IP address of Server class socket in lib.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
An update has been made to the apps feature. Fault tolerance has been added for big data, which was contributed by @onuratakan in https://github.com/Naruno/Naruno/pull/1528.

## Auto-Builders
An improvement has been made to the auto_builders feature, reducing the time sleep after installation, which was contributed by @onuratakan in https://github.com/Naruno/Naruno/pull/1524.

## Blockchain
In the blockchain feature, the maximum number of transactions has been increased, which was contributed by @onuratakan in https://github.com/Naruno/Naruno/pull/1525. Additionally, a new setting has been added to disable block saving, which was contributed by @onuratakan in https://github.com/Naruno/Naruno/pull/1526.

## Transactions
A bug has been fixed in the transactions feature where self-posting transactions were not working properly. This was contributed by @onuratakan in https://github.com/Naruno/Naruno/pull/1523.

## Node
The node feature has been updated with a new exception to bypass deleting buffer of data for situations where there is enough data size. This was contributed by @onuratakan in https://github.com/Naruno/Naruno/pull/1527.

## Packages
The packages feature has been updated to bump werkzeug from version 2.0.3 to 2.2.3. This was contributed by @dependabot in https://github.com/Naruno/Naruno/pull/1458.

## Lib
The lib feature has been updated with a new method to get the IP address of the Server class socket. This was contributed by @cpyberry in https://github.com/Naruno/Naruno/pull/1465.

# 0.51.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Added fault tolerance for big datas by @onuratakan in https://github.com/Naruno/Naruno/pull/1528
### Auto-Builders
* auto_builders: Reduced time sleep after installation by @onuratakan in https://github.com/Naruno/Naruno/pull/1524
### Blockchain
* blockchain: Max tx number increased by @onuratakan in https://github.com/Naruno/Naruno/pull/1525
* blockchain: Added a setting for disabling block saving by @onuratakan in https://github.com/Naruno/Naruno/pull/1526
### Transactions
* transactions: Fixed self-posting transactions by @onuratakan in https://github.com/Naruno/Naruno/pull/1523
### Node
* node: Added bypass exception fr deleting buffer of data for enough data size situations by @onuratakan in https://github.com/Naruno/Naruno/pull/1527
### Packages
* packages: Bump werkzeug from 2.0.3 to 2.2.3 by @dependabot in https://github.com/Naruno/Naruno/pull/1458
### Lib
* lib: Added a method to get the IP address of Server class socket by @cpyberry in https://github.com/Naruno/Naruno/pull/1465


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.50.1-alpha...v0.51.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- @cpyberry
