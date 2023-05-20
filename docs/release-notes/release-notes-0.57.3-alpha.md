---
title: 0.57.3-alpha
parent: Release Notes
nav_order: 134
---

# 0.57.3-alpha Release Notes

The latest version of Naruno, v0.57.3-alpha, includes updates to various components of the network. These changes include redesigning logging functions for blockchain, transactions, node, and API, as well as adding and fixing multiple tests. Additionally, the library has been updated with a license and certain unused imports and import * statements have been removed. 

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
The `get_block` function logger's design has been updated by @onuratakan in https://github.com/Naruno/Naruno/pull/1618.

## Transactions
Redesigned loggers for the `send` function by @onuratakan in https://github.com/Naruno/Naruno/pull/1617.

## Node
All loggings have been redesigned by @onuratakan in https://github.com/Naruno/Naruno/pull/1609. Additionally, custom id settings have been moved to the initialization of the server by @onuratakan in https://github.com/Naruno/Naruno/pull/1612.

## API
Redesigned info logs by @onuratakan in https://github.com/Naruno/Naruno/pull/1616, and 404 loggers have been changed to logger.debug by @onuratakan in https://github.com/Naruno/Naruno/pull/1619.

## Tests
Tests for the Integration.send_forcer function have been added by @onuratakan in https://github.com/Naruno/Naruno/pull/1604. Fixed some time errors of test_blockchain_sync_empty_blocks_first_and_second_empty_is_equal, added unit tests for Integration splited send system, and fixed the test_blockchain_sync_empty_blocks_first_and_second_empty_is_equal by @onuratakan in https://github.com/Naruno/Naruno/pull/1605, https://github.com/Naruno/Naruno/pull/1606, and https://github.com/Naruno/Naruno/pull/1610, respectively.

## Licence
The Naruno import and export libraries have been updated with a license by @onuratakan in https://github.com/Naruno/Naruno/pull/1608.

## Lib
Safety logs have been redesigned by @onuratakan in https://github.com/Naruno/Naruno/pull/1615.

## Other Changes
Unused imports have been removed by @onuratakan in https://github.com/Naruno/Naruno/pull/1607, and `import *` has been removed by @onuratakan in https://github.com/Naruno/Naruno/pull/1611.

# 0.57.3-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Blockchain
* blockchain: get_block function logger.info's redesigned by @onuratakan in https://github.com/Naruno/Naruno/pull/1618
### Transactions
* transactions: send function loggers redesigned by @onuratakan in https://github.com/Naruno/Naruno/pull/1617
### Node
* node: All loggings are redesigned by @onuratakan in https://github.com/Naruno/Naruno/pull/1609
* node:  Custom id settings moved to init of server by @onuratakan in https://github.com/Naruno/Naruno/pull/1612
### API
* api: Redesigned info logs by @onuratakan in https://github.com/Naruno/Naruno/pull/1616
* api: 404 loggers changed with logger.debug by @onuratakan in https://github.com/Naruno/Naruno/pull/1619
### Tests
* tests: Added test for Integration.send_forcer function by @onuratakan in https://github.com/Naruno/Naruno/pull/1604
* tests: Fixed some time errors of test_blockchain_sync_empty_blocks_first_and_second_empty_is_equal by @onuratakan in https://github.com/Naruno/Naruno/pull/1605
* tests: Added unit tests for Integration splited send system by @onuratakan in https://github.com/Naruno/Naruno/pull/1606
* tests: Fixed test_blockchain_sync_empty_blocks_first_and_second_empty_is_equal by @onuratakan in https://github.com/Naruno/Naruno/pull/1610
### Licence
* licence: Added licence to naruno import and export libraries by @onuratakan in https://github.com/Naruno/Naruno/pull/1608
### Lib
* lib: Redesigned safety logs by @onuratakan in https://github.com/Naruno/Naruno/pull/1615
### Other Changes
* Removed unused imports by @onuratakan in https://github.com/Naruno/Naruno/pull/1607
* Removed the `import *` by @onuratakan in https://github.com/Naruno/Naruno/pull/1611


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.57.2-alpha...v0.57.3-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
