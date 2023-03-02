---
title: 0.23.0-alpha
parent: Release Notes
nav_order: 49
---

# 0.23.0-alpha Release Notes

With this minor release we added many well feature and fix.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

We deprecated python version 3.7 and we recommend to use python version 3.8 at least.

# Notable changes

## Security 
If pywall is installed, we will use it to check the system attack status.

## Builds
Closed the console for gui build.

## Wallet
Wallet system synced with ecdsa-python library.

## Block
We added new version of Green Paper as sha256 and validating time added 
to reset operation. Finaly we added a space for block time for calculating 
operations.

## Transaction
We removed a print from SendTransactiontoTheBlock function.

## Node
We added sending full account and blocks hash in send me block function.

## Docker
We maded code quality improvements and fixes in docker images.

## Setup-Setups-GitHub
Changed the required python version to 3.8 at least.

## Documentation
We added some badge and some missing parts and fix in documentation sections.

## Tests
We added docker based functional test and we changed the test names.

## GitHub
Added status information to functional and stability tests. We changed some trigger function and artifact name.

# 0.23.0-alpha change log

### Security
* security: Added pywall library based safety check process by @onuratakan in https://github.com/Naruno/Naruno/pull/526
### Builds
* builds: Closed console in GUI-win32.spec by @bcanergul06 in https://github.com/Naruno/Naruno/pull/520
### Wallet
* wallet: Maded improvements and synced with ecdsa python by @onuratakan in https://github.com/Naruno/Naruno/pull/564
### Block
* block: Added new version of Green Paper as sha256 by @onuratakan in https://github.com/Naruno/Naruno/pull/492
* block: Added validating time reset in block reset by @onuratakan in https://github.com/Naruno/Naruno/pull/556
* block: Added a space from consensus process and block time by @onuratakan in https://github.com/Naruno/Naruno/pull/558
### Transactions
* transactions: Removed the print function of send_transaction_to_the_block by @bcanergul06 in https://github.com/Naruno/Naruno/pull/545
### Node
* node: Added send full accounts and blocks hash to send full chain by @onuratakan in https://github.com/Naruno/Naruno/pull/566
### Docker
* docker: Code quality improvements for api dockerfiles by @onuratakan in https://github.com/Naruno/Naruno/pull/541
* docker: Fixed code quality issues of cli dockerfiles by @onuratakan in https://github.com/Naruno/Naruno/pull/542
### Setup
* setup-setups-github: Changed required python version with at leas 3.8 by @onuratakan in https://github.com/Naruno/Naruno/pull/543
### Documentation
* docs: Added With Copilot badge to README.md by @onuratakan in https://github.com/Naruno/Naruno/pull/496
* docs: Changed the docs site link in README.md by @onuratakan in https://github.com/Naruno/Naruno/pull/499
* docs: Added build badge by @onuratakan in https://github.com/Naruno/Naruno/pull/501
* docs: Added missing parts and nav order to release notes by @onuratakan in https://github.com/Naruno/Naruno/pull/546
### Tests
* tests: Changed the test names by @onuratakan in https://github.com/Naruno/Naruno/pull/549
* tests: Added docker based functional test by @onuratakan in https://github.com/Naruno/Naruno/pull/551
### GitHub
* github: Artifact name changed for gource action by @bcanergul06 in https://github.com/Naruno/Naruno/pull/521
* github: Changed Deploy worfklow run trigger to release publish trigger by @bcanergul06 in https://github.com/Naruno/Naruno/pull/522
* github: Changed build to builds by @onuratakan in https://github.com/Naruno/Naruno/pull/524
* github: Changed Deploy workflow run trigger to release publish trigger for stability tests by @bcanergul06 in https://github.com/Naruno/Naruno/pull/539
* github: Fixed tralling space issues in release.yml by @onuratakan in https://github.com/Naruno/Naruno/pull/540
* github: Added Deploy environment to Deploy workflow by @onuratakan in https://github.com/Naruno/Naruno/pull/544
* github: Added status information to functional tests by @onuratakan in https://github.com/Naruno/Naruno/pull/554
* github: Added Status Information to stability tests by @onuratakan in https://github.com/Naruno/Naruno/pull/559
* github: Added log as artifacts for docker based functional test job by @onuratakan in https://github.com/Naruno/Naruno/pull/562

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- Bahri Can ERGUL
