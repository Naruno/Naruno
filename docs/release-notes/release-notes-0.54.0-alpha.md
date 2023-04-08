---
title: 0.54.0-alpha
parent: Release Notes
nav_order: 119
---

# 0.54.0-alpha Release Notes

Naruno has released a new minor version, v0.54.0-alpha, with several changes and improvements to its apps, blockchain, API, and documentation sections. Among the new features are the ability to send multiple transactions to the same blockchain, a new section for checking recent transactions, and a checker thread mode in the apps section. In the blockchain category, users can now disable just one transaction from the same addresses. Additionally, a new API has been added that allows users to retrieve information about a single transaction from the blockchain. Finally, the documentation section has been updated with fixed Codebeat badges for improved user experience. 

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
The latest update has added some new features to the apps section of Naruno. Users can now send multiple transactions to the same blockchain, and there is a new section for checking the last max_tx_number/2 transactions. Additionally, a checker thread mode has been introduced for improved performance.

## Blockchain
In the blockchain category, a new feature has been added that allows users to disable just one transaction from the same addresses. This can be particularly useful when dealing with complex transactions.

## API
There is a new API added in this release, which is the /blockjustonetx get API. This API provides users with the ability to retrieve information about a single transaction from the blockchain.

## Docs
The latest update has fixed the Codebeat badges in the documentation section, improving the overall user experience.

# 0.54.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Added ability to sending multiple tx to same blockchain by @onuratakan in https://github.com/Naruno/Naruno/pull/1562
* apps: Added a section for checking last max_tx_number/2 transactions by @onuratakan in https://github.com/Naruno/Naruno/pull/1563
* apps: Added checker thread mode
### Blockchain
* blockchain: Added disabling just one transaction from same addresses by @onuratakan in https://github.com/Naruno/Naruno/pull/1561
### API
* api: Added /blockjustonetx get api by @onuratakan in https://github.com/Naruno/Naruno/pull/1564
### Docs
* docs: Codebeat badges fixed by @onuratakan in https://github.com/Naruno/Naruno/pull/1559


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.53.0-apha...v0.54.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
