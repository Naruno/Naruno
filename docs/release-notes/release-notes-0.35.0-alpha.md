---
title: 0.35.0-alpha
parent: Release Notes
nav_order: 70
---

# 0.35.0-alpha Release Notes

With this minor release we added syncing mechanism that about gap blocks, and we change policy of minumum amount of transaction, also we add a video for node concept, some other docs are added and fixed gap and hard block releationship.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
We fix the gap block and hard block relationship, and we add syncing mechanism that starts in every gap block.

## Transactions
With this release we change the policy that not controll if the recipient account have enough balance to receive the transaction we not check the transaction amount.


## Docs
We added these docs:
- Hard Blocks
- Gap Blocks
- Syncing Operations

and we added video for node concept with manim.

# 0.35.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Blockchain
* blockchain: Gap block number is fixed with + hard block number by @onuratakan in https://github.com/Naruno/Naruno/pull/1214
* blockchain: Added syncing with the network by @onuratakan in https://github.com/Naruno/Naruno/pull/1215
### Transactions
* transactions: Added controlling the touser balance for just data sended transactions, if balance is enough we shouldn't check and add minumum transfer amount by @onuratakan in https://github.com/Naruno/Naruno/pull/1221
### Docs
* docs: Added Node concept video by @onuratakan in https://github.com/Naruno/Naruno/pull/1217
* docs: Added types of blocks by @onuratakan in https://github.com/Naruno/Naruno/pull/1218
* docs: Added syncing docs by @onuratakan in https://github.com/Naruno/Naruno/pull/1219
* docs: Changed block time and added a note for some features by @onuratakan in https://github.com/Naruno/Naruno/pull/1220


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.34.0-alpha...v0.35.0-alpha


# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
