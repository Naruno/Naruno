---
title: 0.38.0-alpha
parent: Release Notes
nav_order: 75
---

# 0.38.0-alpha Release Notes

With this minor release we add a backend system for saving first blockshash part and first block to blockchain db.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Accounts
We add a try except situation for looking baalnce of an account via GetBalance method. If the block is not found, it will return None.

## Blockchain
We add logging for ChangeTransactionFee function.

## Transactions
We add notification when a transaction is came or send or validated. Also we add logging to PendingtoValidating function.

## Node
We add logging to server.check_connected and server.run function.

## Consensus
We add logging to many system of consensus, you can see it in the below change log.

## Packages
We removed `cgitb` import for preventing error.

## Docs
We add supported os and sponsors to readme file.

## Tests
Fixed unl node test and increased expexted time of consensus_trigger function.

## GitHub
Devksim has been removed for preventing false alerts, also we remove cache from buildozer jobs and we re-add gource.

## GUI
We fix all bugs that caused by the library updates. Also we add QR code feature for address and node id, we moved address copy to a button for address. Lastly we add a settings for muting notifications.

## Lib
We fix multiple logging bug and we add QR code, notification and backup system.



# 0.38.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Accounts
* accounts: Fixed FileNotFoundError from GetBalance from GetBlock function by @onuratakan in https://github.com/Naruno/Naruno/pull/1311
### Blockchain
* blockchain: Added logging to ChangeTransactionFee function by @alieren196 in https://github.com/Naruno/Naruno/pull/1245
### Transactions
* transactions: Added logging to PendingtoValidating function by @alieren196 in https://github.com/Naruno/Naruno/pull/1239
* transactions: Notification on validated and received and sended transaction by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1312
### Node
* node: Added logging to server.check_connected function by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1238
* node: Added logging to server.run function by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1247
### Consensus
* consensus: Added logging to time control of round 1 by @alieren196 in https://github.com/Naruno/Naruno/pull/1250
* consensus: Added logging to time control of round 2 by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1253
* consensus: Added logging to candidate block control of round 2 by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1255
* consensus: Added logging to check main of round 2  by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1258
* consensus: Adding logging to validate main of round 2 by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1272
* consensus: Added logging to remove duplicates of round 1 by @alieren196 in https://github.com/Naruno/Naruno/pull/1275
* consensus: Added logging to process main of round 2 by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1281
* consensus: Added logging to process candidate block hashes of round 2 by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1278
* consensus: Added logging to find validated of round 1 by @alieren196 in https://github.com/Naruno/Naruno/pull/1277
* consensus: Added logging to find newly of round 1 by @alieren196 in https://github.com/Naruno/Naruno/pull/1276
* consensus: Added logging to rescue main of round 2 by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1280
* consensus: Added logging to process transaction of round 1 by @alieren196 in https://github.com/Naruno/Naruno/pull/1279
* consensus: Added logging to main of round 2 by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1285
* consensus: Added logging to candidate block control of round 1 by @onuratakan in https://github.com/Naruno/Naruno/pull/1290
* consensus: Added logging to check main of round 1 by @onuratakan in https://github.com/Naruno/Naruno/pull/1292
* consensus: Added logging to process main of round 1 by @onuratakan in https://github.com/Naruno/Naruno/pull/1293
* consensus: Added logging to  main of round 1 by @alieren196 in https://github.com/Naruno/Naruno/pull/1298
### Packages
* packages: Removed unused cgitb reset function for fixing bugs on packages by @onuratakan in https://github.com/Naruno/Naruno/pull/1288
### Docs
* docs: Added supported OS to readme by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1319
* docs: Added sponsors to readme by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1320
### Tests
* tests: Fixed not unl node test by @onuratakan in https://github.com/Naruno/Naruno/pull/1282
* tests: Increased consensus_trigger expected time to 2 by @onuratakan in https://github.com/Naruno/Naruno/pull/1283
### GitHub
* github: Enabled resltyled pull request for forks based pull requests by @onuratakan in https://github.com/Naruno/Naruno/pull/1259
* github: Revert "github: Enabled resltyled pull request for forks based pull requests" by @onuratakan in https://github.com/Naruno/Naruno/pull/1260
* github: Removed devskim for preventing false alerts by @onuratakan in https://github.com/Naruno/Naruno/pull/1274
* github: Removed caching from buildozer by @onuratakan in https://github.com/Naruno/Naruno/pull/1307
* github: Added gource action by @onuratakan in https://github.com/Naruno/Naruno/pull/1315
### GUI
* gui: Fixed button text bug after updating requirements by @onuratakan in https://github.com/Naruno/Naruno/pull/1302
* gui: Added address to QR code transformation by @alieren196 in https://github.com/Naruno/Naruno/pull/1304
* gui: Added node id to QR code transformation by @onuratakan in https://github.com/Naruno/Naruno/pull/1308
* gui: Moved address copy to a button by @onuratakan in https://github.com/Naruno/Naruno/pull/1309
* gui: Added mute notifications setting by @alieren196 in https://github.com/Naruno/Naruno/pull/1317
### Lib
* lib: Fixed multiple times same logging by @onuratakan in https://github.com/Naruno/Naruno/pull/1242
* lib: Added QR module by @alieren196 in https://github.com/Naruno/Naruno/pull/1299
* lib: Added notification module by @bcanergul06 in https://github.com/Naruno/Naruno/pull/1300
* lib: Added backup system by @alieren196 in https://github.com/Naruno/Naruno/pull/1318


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.37.0-alpha...v0.38.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- Bahri Can ERGÜL
- Ali Eren TABAK
