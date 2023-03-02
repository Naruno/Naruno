---
title: 0.40.0-alpha
parent: Release Notes
nav_order: 77
---

# 0.40.0-alpha Release Notes

With this minor release we fix the all of consensus proccess and also we fix releated system for consensus correction and working. Also we added backup ability to CLI, added data sending ability to GUI, Fixed GUI bugs   , we add some API's, fixed packge problem and added some docs. And we add high fault tolerance for consensus in node system.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
Removed empty block number from hash calculation and added many element of block to hash calculation. Changed saving and getting system for block. Removed candidate block resetting. Also changed share transactions time with block.start_time.

## Transactions
Fixed some bugs that caused by share transactions.

## CLI
Added backup ability.

## Node
Added try excepts for preventing closing sockets. And added historical candidate blocks.

## API
Added export block api and added cors settins for getting some safe info for healty.

## Consensus
Added self candidate block for round 1 and 2, candidate block sending moved to thread that start of end of consensus_main. All checks are set to majority.

## Package
Fixed console scripts bug.

## Docs
Removed lgtm from readme, removed gui macos download link. Added user interfaces, video index and usag documents.

## GUI
Added data sending ability and fixed FileNotFound and NoneType errors.

## Lib
Added cleaning test_app outputs and sended variable to export transactions csv and added some error suppress for perpetualtimer.

# 0.40.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Blockchain
* blockchain: Removed empty block number from hash calculation by @onuratakan in https://github.com/Naruno/Naruno/pull/1368
* blockchain: Changed share transactions from users for sorting by @onuratakan in https://github.com/Naruno/Naruno/pull/1376
* blockchain: Changed transaction time with block.start_time for share transactions by @onuratakan in https://github.com/Naruno/Naruno/pull/1379
* blockchain: Added double saving for SaveBlock by @onuratakan in https://github.com/Naruno/Naruno/pull/1383
* blockchain: Removed candidate block resetting by @onuratakan in https://github.com/Naruno/Naruno/pull/1387
* Revert "blockchain: Removed candidate block resetting" by @onuratakan in https://github.com/Naruno/Naruno/pull/1388
* blockchain: Added transaction fee based values to calculating hash by @onuratakan in https://github.com/Naruno/Naruno/pull/1402
### Transactions
* transactions: Added cleaning signature == "DN" transactions before share transactions by @onuratakan in https://github.com/Naruno/Naruno/pull/1374
### CLI
* cli: Added backup system functions by @onuratakan in https://github.com/Naruno/Naruno/pull/1332
### Node
* node: Added an exit the message reception loop when a destination node is closed by @cpyberry in https://github.com/Naruno/Naruno/pull/1329
* node: Added socket.timeout suppress for send_client function by @onuratakan in https://github.com/Naruno/Naruno/pull/1360
* node: Stored last 5 candidate blocks and getting by sequance number by @onuratakan in https://github.com/Naruno/Naruno/pull/1399
### API
* api: Added api for gathering the block as json by @onuratakan in https://github.com/Naruno/Naruno/pull/1346
* api: CORS settings have been set by @onuratakan in https://github.com/Naruno/Naruno/pull/1348
### Consensus
* consensus: Added the self to round 1 find validated transactions voting by @onuratakan in https://github.com/Naruno/Naruno/pull/1362
* consensus: Increased circulation time to 1.50s by @onuratakan in https://github.com/Naruno/Naruno/pull/1366
* consensus: Moved candidate block sending to the start of rounds by @onuratakan in https://github.com/Naruno/Naruno/pull/1370
* consensus: Moved candidate block sending to the start of consensus_main by @onuratakan in https://github.com/Naruno/Naruno/pull/1372
* consensus: Reverted cadidate block sending by @onuratakan in https://github.com/Naruno/Naruno/pull/1377
* consensus: Increased circulation time to 2s by @onuratakan in https://github.com/Naruno/Naruno/pull/1382
* Revert "consensus: Reverted cadidate block sending" by @onuratakan in https://github.com/Naruno/Naruno/pull/1385
* consensus: Added self adding to canddiate block checks by @onuratakan in https://github.com/Naruno/Naruno/pull/1389
* consensus: All systems assigned to majority by @onuratakan in https://github.com/Naruno/Naruno/pull/1391
### Packages
* packages: Fixed console script bug by adding .main before using start function by @onuratakan in https://github.com/Naruno/Naruno/pull/1340
### Docs
* docs: Removed lgtm from readme by @onuratakan in https://github.com/Naruno/Naruno/pull/1342
* docs: Fixed codacy badge on readme by @onuratakan in https://github.com/Naruno/Naruno/pull/1344
* docs: Added user interfaces to concepts by @alieren196 in https://github.com/Naruno/Naruno/pull/1351
* docs: Added usage docs to getting started by @alieren196 in https://github.com/Naruno/Naruno/pull/1354
* docs: Added Videos index by @alieren196 in https://github.com/Naruno/Naruno/pull/1355
* docs: Some typo fixes by @omahs in https://github.com/Naruno/Naruno/pull/1384
* docs: Removed gui macos from installations by @alieren196 in https://github.com/Naruno/Naruno/pull/1400
### GUI
* gui: Added ability to send data by @onuratakan in https://github.com/Naruno/Naruno/pull/1334
* gui: Fixed FileNotFoundError for GetBlock function usage by @onuratakan in https://github.com/Naruno/Naruno/pull/1335
* gui: Fixed NoneType errors that caused by server.Server by @onuratakan in https://github.com/Naruno/Naruno/pull/1337
### Lib
* lib: Added cleaning test_app outputs by @onuratakan in https://github.com/Naruno/Naruno/pull/1331
* lib: Added sended variable to export transaction csv by @onuratakan in https://github.com/Naruno/Naruno/pull/1333
* lib: Added suppress to perpetualtimer by @onuratakan in https://github.com/Naruno/Naruno/pull/1364

## New Contributors
* @omahs made their first contribution in https://github.com/Naruno/Naruno/pull/1384

**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.39.0-alpha...v0.40.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- Ali Eren TABAK
- @cpyberry
- @omahs

