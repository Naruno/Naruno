---
title: 0.26.0-alpha
parent: Release Notes
nav_order: 52
---

# 0.26.0-alpha Release Notes

With this minor release we increased our testing amount and we are 
added mobile packaging (Android). And we maded many improvements.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

## OLD GUI Requirements
Kivy==2.0.0
kivymd==0.104.1

## NEW GUI Requirements
Kivy==2.1.0
kivymd==0.104.2

# Notable changes

## Builds
Added these builds and automated:
- MacOS CLI
- MacOS API
- Android API
- Android GUI

## Node
The all of node system removed and wrote a new system.

## Docs
Added codecov badge.

## Tests
Added many unit tests (%53.51 to %92.72).

## GitHub
Added codecov.


# 0.26.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Builds
* builds: Synced with new folder and import structure by @onuratakan in https://github.com/Naruno/Naruno/pull/821
* builds: Added Android API build by @onuratakan in https://github.com/Naruno/Naruno/pull/880
* builds: Added Android GUI build (Compatility Changes !) by @onuratakan in https://github.com/Naruno/Naruno/pull/884
* builds: Added MacOS CLI and API builds by @onuratakan in https://github.com/Naruno/Naruno/pull/887
### Wallet
* wallets: Removed create_a_wallet.py by @onuratakan in https://github.com/Naruno/Naruno/pull/614
* wallet: Removed print_balance.py by @onuratakan in https://github.com/Naruno/Naruno/pull/629
* wallet: Removed unused parts by @onuratakan in https://github.com/Naruno/Naruno/pull/859
### Auto-Builders
* auto_builders: Decreased the sleep time after build by @onuratakan in https://github.com/Naruno/Naruno/pull/760
### Transactions
* transactions: Removed SendTransactiontoTheBlock function by @onuratakan in https://github.com/Naruno/Naruno/pull/685
### Node
* node: Deleted disconnect_to_node function of Node class by @onuratakan in https://github.com/Naruno/Naruno/pull/782
* node: Changed connected node saving mechanism for preventing writing in same time by @onuratakan in https://github.com/Naruno/Naruno/pull/816
* node: Added a forwadder for send function to send_client by @onuratakan in https://github.com/Naruno/Naruno/pull/820
* node: Removed not exist situation of get_connected_nodes function of server by @onuratakan in https://github.com/Naruno/Naruno/pull/847
### Setup
* setup-setups: Library Package Improved #801 by @onuratakan in https://github.com/Naruno/Naruno/pull/807
* setup and gui: minor improvements by @keyiflerolsun in https://github.com/Naruno/Naruno/pull/809
### Documentations
* docs: Added codecov badge to README.md by @onuratakan in https://github.com/Naruno/Naruno/pull/597
### Tests
* tests: Added unit tests for wallet_selector function by @onuratakan in https://github.com/Naruno/Naruno/pull/608
* tests: Added unit tests for delete_current_wallet function by @onuratakan in https://github.com/Naruno/Naruno/pull/611
* tests: Adding unit test for my transaction functions by @onuratakan in https://github.com/Naruno/Naruno/pull/622
* tests: Added unit tests for dumb and load json transaction by @onuratakan in https://github.com/Naruno/Naruno/pull/626
* tests: Added unit test for print_wallets function if not current_wallet == number situation by @onuratakan in https://github.com/Naruno/Naruno/pull/632
* tests: Maded code quality improvements for test files by @onuratakan in https://github.com/Naruno/Naruno/pull/636
* tests: Added unit test for wallet_delete function if account in saved_wallet else situation by @onuratakan in https://github.com/Naruno/Naruno/pull/640
* tests: Added unit test for wallet_import function if not -1 == account else situation by @onuratakan in https://github.com/Naruno/Naruno/pull/644
* tests: Added unit test for wallet_import if not password is None and not list(temp_saved_wallet).index(account) == 0 else situation by @onuratakan in https://github.com/Naruno/Naruno/pull/647
* tests: Adding unit test for wallet_import mode == 2 situation by @onuratakan in https://github.com/Naruno/Naruno/pull/651
* tests: Adding unit test for wallet_import not true mode number situation and fixed test 16 in test_wallet.py by @onuratakan in https://github.com/Naruno/Naruno/pull/654
* tests: Added unit test for PendinttoValidating function and changed with PendingtoValidating and fixed the block previous hash by @onuratakan in https://github.com/Naruno/Naruno/pull/657
* tests: Added unit test for TXAlreadyGot function by @onuratakan in https://github.com/Naruno/Naruno/pull/661
* tests: Added unit tests for ChangeTransactionFee function by @onuratakan in https://github.com/Naruno/Naruno/pull/665
* tests: Added unit test for account class and removed test numbers by @onuratakan in https://github.com/Naruno/Naruno/pull/672
* tests: Added unit tests for CheckTransaction function and checking transaction system redesigned by @onuratakan in https://github.com/Naruno/Naruno/pull/678
* tests: Added some unit_tests for send function by @onuratakan in https://github.com/Naruno/Naruno/pull/688
* tests: Added some tests for block.reset_the_block function by @onuratakan in https://github.com/Naruno/Naruno/pull/693
* tests: Added unit tests for CalculateHash and redesigned hash calculation system by @onuratakan in https://github.com/Naruno/Naruno/pull/697
* tests: Adding some unit tests for Block.reset_the_block function by @onuratakan in https://github.com/Naruno/Naruno/pull/701
* tests: Redesigned and added unit tests to GetTransaction and send function by @onuratakan in https://github.com/Naruno/Naruno/pull/704
* tests: Redesigned and added unit tests for ProccesstheTransaction by @onuratakan in https://github.com/Naruno/Naruno/pull/710
* tests: GetBalance function redesigned and added unit tests by @alieren196 in https://github.com/Naruno/Naruno/pull/714
* tests: Added unit tests for GetSequanceNumber function by @onuratakan in https://github.com/Naruno/Naruno/pull/717
* tests: Added unit tests for SaveAccounts and GetAccounts functions by @onuratakan in https://github.com/Naruno/Naruno/pull/723
* tests: Added unit tests for SaveBlock and GetBlock functions by @onuratakan in https://github.com/Naruno/Naruno/pull/728
* tests: Added unit tests for SaveBlockshash, SaveBlockshash_part, GetBlockshash, GetBlockshash_part functions by @onuratakan in https://github.com/Naruno/Naruno/pull/735
* tests: Added unit test for candidate_block and GetCandidateBlocks functions by @onuratakan in https://github.com/Naruno/Naruno/pull/740
* tests: Added unit test for SaveBlockstoBlockchainDB and GetBlockstoBlockchainDB function by @onuratakan in https://github.com/Naruno/Naruno/pull/745
* tests: Added unit tests for CreateBlock function by @onuratakan in https://github.com/Naruno/Naruno/pull/750
* tests: Added unit tests for app class and AppsTrigger function by @onuratakan in https://github.com/Naruno/Naruno/pull/756
* tests: Added unit test fpr dump and load json functions of Block class by @onuratakan in https://github.com/Naruno/Naruno/pull/768
* tests: Added unit test for if not current_block.hash is None situation of CreateBlock function by @onuratakan in https://github.com/Naruno/Naruno/pull/772
* transaction: Developed a pending transaction controlling system for preventing writing in same time by @onuratakan in https://github.com/Naruno/Naruno/pull/777
* tests: Added unit tests for parse_packet function of Connection class by @onuratakan in https://github.com/Naruno/Naruno/pull/789
* tests: Added unit tests for connection.py by @onuratakan in https://github.com/Naruno/Naruno/pull/794
* tests: Added unit test for Address function by @onuratakan in https://github.com/Naruno/Naruno/pull/796
* tests: Added unit tests for if not Unl.node_is_unl(connected_node_id) situation of run and connect_to_node functions of Node class by @onuratakan in https://github.com/Naruno/Naruno/pull/799
* tests: Merged all node unit tests that start and close Node and Connection in one test by @onuratakan in https://github.com/Naruno/Naruno/pull/812
* tests: Added unit test for send_full_chain get_full_chain functions of server by @onuratakan in https://github.com/Naruno/Naruno/pull/823
* tests: Added unit tests for send full accounts and get full accounts functions by @onuratakan in https://github.com/Naruno/Naruno/pull/824
* test: Added unit tests for send_full_blockcshash get_full_blockshash functions of server by @onuratakan in https://github.com/Naruno/Naruno/pull/827
* tests: Adding unit tests for send full blockshash_part and get full blockshash_part functions by @onuratakan in https://github.com/Naruno/Naruno/pull/829
* test: Addint unit tests for testing different situations of send and get block, accounts, blockshash, blockshash_part functions of server by @onuratakan in https://github.com/Naruno/Naruno/pull/832
* tests: Added unit tests for false messages types of server system by @onuratakan in https://github.com/Naruno/Naruno/pull/834
* tests: Added unit test for socket.timeout situation of server.connect function by @onuratakan in https://github.com/Naruno/Naruno/pull/845
* tests: Added test_connectionfrommixdb and test_connected_node_delete_and_save in test_node by @onuratakan in https://github.com/Naruno/Naruno/pull/851
* tests: Added unit test for send and get transactions of server by @onuratakan in https://github.com/Naruno/Naruno/pull/852
* tests: Added unit tests for send_block_to_other_nodes and send_me_full_block function by @onuratakan in https://github.com/Naruno/Naruno/pull/853
* tests: Added unit tests for send_my_block and get_candidate_block functions of server by @onuratakan in https://github.com/Naruno/Naruno/pull/854
* tests: Added unit test for send and get candidate block hash by @onuratakan in https://github.com/Naruno/Naruno/pull/856
* tests: Added unit test for os path not exist situation of get_unl_nodes by @onuratakan in https://github.com/Naruno/Naruno/pull/857
* tests: Added unit test for not in list wallet number situation of wallet_import by @onuratakan in https://github.com/Naruno/Naruno/pull/861
* tests: Decreased time sleeps for node system testing by @onuratakan in https://github.com/Naruno/Naruno/pull/862
### GitHub
* github: Added codecov by @onuratakan in https://github.com/Naruno/Naruno/pull/594
* github: Changed Github-Actions label to GitHub by @onuratakan in https://github.com/Naruno/Naruno/pull/600
* github: Changed the name and job name of gource.yml by @onuratakan in https://github.com/Naruno/Naruno/pull/601
* github: Changed test labels to tests and removed test_environments by @onuratakan in https://github.com/Naruno/Naruno/pull/625
* github: Changed cli menu and paremeters label to CLI by @onuratakan in https://github.com/Naruno/Naruno/pull/676
* github: APP label changed to APPS by @onuratakan in https://github.com/Naruno/Naruno/pull/765
* github: Changed Documatation label to Docs by @onuratakan in https://github.com/Naruno/Naruno/pull/878
### Other Changes
* Changed pickle saving methods to json by @onuratakan in https://github.com/Naruno/Naruno/pull/762
* 🕊 Some Refactorings For Clean Code by @keyiflerolsun in https://github.com/Naruno/Naruno/pull/775
* Revert "node: Deleted disconnect_to_node function of Node class" by @onuratakan in https://github.com/Naruno/Naruno/pull/784
* Some Refactorings For Clean Code Part 2 by @keyiflerolsun in https://github.com/Naruno/Naruno/pull/786

## New Contributors
* @alieren196 made their first contribution in https://github.com/Naruno/Naruno/pull/714
* @keyiflerolsun made their first contribution in https://github.com/Naruno/Naruno/pull/775

**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.25.0-alpha...v0.26.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- Ali Eren TABAK
- @keyiflerolsun
