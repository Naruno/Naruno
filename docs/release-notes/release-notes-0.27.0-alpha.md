---
title: 0.27.0-alpha
parent: Release Notes
nav_order: 54
---

# 0.27.0-alpha Release Notes

With this minor release we increase code coverage to 100%. We also made some scalability improvements by performance and maded some other improvements.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Accounts

Changed the saving method to sqlite3 and reduced maximum number of
accounts to 10000 by reducing coin amount.

## Blockchain

Removed edited accounts based hash calculation for more durability.

## Transactions

Created a function for performance improvement and removed a functions that useless.

## Node

Added buffer mechanism and fixed to 6525 bytes and added timestamp control for security reasons and fixed to 10 seconds.

## Consensus

Maded many code quality improvements by dividing the code into smaller parts.

## Docs

Added cloudback.it and deploy badge.

## Tests

Added many tests for 100% code coverage.

## GitHub

Maded many improvements and fix for Actions and maded some other improvements.

## Other Changes

Removed sequance number from node system and added empty block number to hash calculation for more durability.

# 0.27.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed

### Accounts

- accounts: Reduced maxiumum Account number by @onuratakan in https://github.com/Naruno/Naruno/pull/939
- accounts: Used sqlite3 for account by @onuratakan in https://github.com/Naruno/Naruno/pull/971

### Blockchain

- blockchain: Removed edited accounts value by @onuratakan in https://github.com/Naruno/Naruno/pull/937

### Transactions

- transactions: Created a GetPendingAmount function for using in just len needed situation like ChangeTransactionFee by @onuratakan in https://github.com/Naruno/Naruno/pull/982
- transactions: Removed same pendings to get pendings functions by @onuratakan in https://github.com/Naruno/Naruno/pull/983

### Node

- node: Added buffer adder for preventing errors by @onuratakan in https://github.com/Naruno/Naruno/pull/978
- node: Added time to sending data for more security by @onuratakan in https://github.com/Naruno/Naruno/pull/1058

### Consensus

- consensus: Improvements for code quality by @onuratakan in https://github.com/Naruno/Naruno/pull/936

### Docs

- docs: Added cloudback.it to README.md by @onuratakan in https://github.com/Naruno/Naruno/pull/898
- docs: Added deploys workflow badge to README.md by @onuratakan in https://github.com/Naruno/Naruno/pull/900

### Tests

- github: Added caching to tests workflow jobs by @onuratakan in https://github.com/Naruno/Naruno/pull/943
- tests: Added unit test for true_time function by @onuratakan in https://github.com/Naruno/Naruno/pull/949
- tests: Added unit test for transactions_main function of finished by @onuratakan in https://github.com/Naruno/Naruno/pull/972
- tests: Added unit test for finished_main function by @onuratakan in https://github.com/Naruno/Naruno/pull/973
- tests: Added unit test for candidate_blocks_check function by @onuratakan in https://github.com/Naruno/Naruno/pull/974
- tests: Added unit test for candidate_blocks_hashes_check function by @onuratakan in https://github.com/Naruno/Naruno/pull/977
- tests: Added unit test for time_difference_check function of round 1 by @onuratakan in https://github.com/Naruno/Naruno/pull/984
- tests: Added unit test for round_check function of round 1 by @onuratakan in https://github.com/Naruno/Naruno/pull/985
- tests: Added unit test for find_newly function by @onuratakan in https://github.com/Naruno/Naruno/pull/986
- tests: Added unit test for find_validated function by @onuratakan in https://github.com/Naruno/Naruno/pull/987
- tests: Added unit test for transactions_main function of round 1 by @onuratakan in https://github.com/Naruno/Naruno/pull/988
- tests: Added unit test for round_process function of round 1 by @onuratakan in https://github.com/Naruno/Naruno/pull/990
- tests: Addedunit test for consensus_round_1 function by @onuratakan in https://github.com/Naruno/Naruno/pull/991
- tests: Added unit test for time_difference_check function of round 2 by @onuratakan in https://github.com/Naruno/Naruno/pull/993
- tests: Added unit test for round_check function of round 2 by @onuratakan in https://github.com/Naruno/Naruno/pull/995
- tests: Added unit test for process_candidate_blocks_hashes function by @onuratakan in https://github.com/Naruno/Naruno/pull/996
- tests: Added unit test for validate_main function by @onuratakan in https://github.com/Naruno/Naruno/pull/997
- tests: Added unit test for rescue_main function by @onuratakan in https://github.com/Naruno/Naruno/pull/998
- tests: Added unit test for round_process function of round 2 by @onuratakan in https://github.com/Naruno/Naruno/pull/999
- tests: Added unit test for consensus_round_2 function by @onuratakan in https://github.com/Naruno/Naruno/pull/1000
- tests: Added unit test for ongoing_main function by @onuratakan in https://github.com/Naruno/Naruno/pull/1001
- tests: Added unit test for consensus_trigger function by @onuratakan in https://github.com/Naruno/Naruno/pull/1002
- tests: Added unit test for mixlib functions by @onuratakan in https://github.com/Naruno/Naruno/pull/1006
- tests: Added unit test for Status function by @onuratakan in https://github.com/Naruno/Naruno/pull/1010
- tests: Added unit test for export_the_transactions function by @onuratakan in https://github.com/Naruno/Naruno/pull/1011
- tests: Added unit test for safety_check function by @onuratakan in https://github.com/Naruno/Naruno/pull/1012
- tests: Added unit test for test_mode function by @onuratakan in https://github.com/Naruno/Naruno/pull/1016
- tests: Added unit test for debug_mode function by @onuratakan in https://github.com/Naruno/Naruno/pull/1017
- tests: Added unit test for perpetualTimer class by @onuratakan in https://github.com/Naruno/Naruno/pull/1018
- tests: Added unit test for wallet_change_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1040
- tests: Added unit test for create_wallet_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1041
- tests: Added unit test for delete_wallets_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1042
- tests: Added unit test for send_coin_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1043
- tests: Added unit test for send_coin_data_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1044
- tests: Added unit test for balance_wallets_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1045
- tests: Added unit test for node_start_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1046
- tests: Added unit test for node_stop_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1047
- tests: Added unit test for node_connect_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1048
- tests: Added unit test for node_connectmixdb_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1049
- tests: Added unit test for node_newunl_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1050
- tests: Added unit test for node_id_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1051
- tests: Adding unit test for settings_test_on_page api and settings_te… by @onuratakan in https://github.com/Naruno/Naruno/pull/1052
- tests: Added unit test for settings_debug_on_page api and settings_debug_off_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1053
- tests: Added unit test for block_get_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1054
- tests: Adding unit test for export_transaction_csv_page and export_transaction_json_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1055
- tests: Added unit test for status_page api by @onuratakan in https://github.com/Naruno/Naruno/pull/1056

### GitHub

- github: Added pull request template by @onuratakan in https://github.com/Naruno/Naruno/pull/895
- github: Added automatic upload the artifacts system by @onuratakan in https://github.com/Naruno/Naruno/pull/903
- github: Fix for automatic adding release asset by @onuratakan in https://github.com/Naruno/Naruno/pull/904
- github: Added automatic labeler for pull requests by @onuratakan in https://github.com/Naruno/Naruno/pull/906
- github: Added caching for build android api and gui jobs by @onuratakan in https://github.com/Naruno/Naruno/pull/907
- github: Added caching for pyinstaller builds by @onuratakan in https://github.com/Naruno/Naruno/pull/911
- github: Disabled some triggers of devskrim and ossar workflows by @onuratakan in https://github.com/Naruno/Naruno/pull/917
- github: Disabled some worflow triggers that run for document files by @onuratakan in https://github.com/Naruno/Naruno/pull/924
- github: Added automatic issue labeler by @onuratakan in https://github.com/Naruno/Naruno/pull/926
- github: Added name for jobs artifacts by @onuratakan in https://github.com/Naruno/Naruno/pull/930
- github: Changed "APPS" label to "Apps" by @onuratakan in https://github.com/Naruno/Naruno/pull/931
- github: Added caching to stability tests by @onuratakan in https://github.com/Naruno/Naruno/pull/945
- github: Added concurrency for workflows by @onuratakan in https://github.com/Naruno/Naruno/pull/947
- github: Added caching for codecov workflow by @onuratakan in https://github.com/Naruno/Naruno/pull/951
- github: Removed archiving logs for preventing errors from github by @onuratakan in https://github.com/Naruno/Naruno/pull/1057

### Other Changes

- Some improvements for empty block numbers by @onuratakan in https://github.com/Naruno/Naruno/pull/1059

**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.26.1-alpha...v0.27.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
