---
title: 0.54.2-alpha
parent: Release Notes
nav_order: 121
---

# 0.54.2-alpha Release Notes

The Naruno team has released a new path, v0.54.2-alpha, with several changes to the blockchain and apps features. These changes include fixing a bug related to unvalidated transactions in the "get" function of the apps feature, increasing the maximum number of transactions to 1000, increasing the block time to 27 seconds, and adding data for block performance calculation. Additionally, several tests have been fixed to ensure the functionality and efficiency of the Naruno blockchain. For more information, please refer to the full changelog on the Naruno Github repository.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
In this release, several changes have been made to the blockchain of Naruno. The maximum number of transactions has been increased from 100 to 1000, which will allow for greater transaction throughput. Additionally, the round 1 time has been increased, and round 2 time has been decreased to make the blockchain more efficient. The block time has also been increased from 22 seconds to 27 seconds, which will provide more time for processing transactions. Finally, data for block performance calculation has been added, which will allow for better monitoring and analysis of the blockchain's performance.

## Apps
The Naruno team has fixed a bug related to unvalidated transactions in the "get" function of the apps feature. This fix was implemented by Onur Atakan and can be found in the Naruno Github repository.

## Tests
Fixed unit tests related to apps, and functional tests was fixed with a custom set max_data_size and max_tx_number with funtionaltest_mode. These tests were implemented by Onur Atakan and can be found in the Naruno Github repository.


# 0.54.2-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Fixed sended not validated txs in get function by @onuratakan in https://github.com/Naruno/Naruno/pull/1566
### Blockchain
* blockchain: Max tx number increased to 1000 by @onuratakan in https://github.com/Naruno/Naruno/pull/1568
* blockchain: Round 1 time increased and round 2 time is decreased by @onuratakan in https://github.com/Naruno/Naruno/pull/1569
* blockchain: Block time increased to 27 second by @onuratakan in https://github.com/Naruno/Naruno/pull/1572
* blockchain: Added data for block performance calculation by @onuratakan in https://github.com/Naruno/Naruno/pull/1573
### Tests
* tests: Fixed apps unit tests by @onuratakan in https://github.com/Naruno/Naruno/pull/1567
* tests: Fixed the functional test with custom set max_data_size and max_tx_number with funtionaltest_mode by @onuratakan in https://github.com/Naruno/Naruno/pull/1571


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.54.1-alpha...v0.54.2-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
