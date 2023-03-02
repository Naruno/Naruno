---
title: 0.33.0-alpha
parent: Release Notes
nav_order: 68
---

# 0.33.0-alpha Release Notes

With this minor release we added cache system for part amount hash calculation and we added Gap and Hard block types.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
We added a cache for not effected blockshash part merkle tree calculations. And we added a concept that named Gap and Hard block types. The Gap blocks are generated for syncing infrastructure and Hard blocks are generated for blocks that calculate the part amount hash.

## Lib
We added hash calculation, transactions and we seperated the Hard and normal block types on performance analyzers.

# 0.33.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Blockchain
* blockchain: Added cache for calculation not effected blockshash part merkle tree by @onuratakan in https://github.com/Naruno/Naruno/pull/1197
* blockchain: Increased block time for every part amount block for calculation new blockshash part merkle (Gap Blocks) by @onuratakan in https://github.com/Naruno/Naruno/pull/1202
* blockchain: Added a area for calculating long part list merkle root calculations (Hard Blocks) by @onuratakan in https://github.com/Naruno/Naruno/pull/1205
### Lib
* lib: Added hash calculation to performance analyzers by @onuratakan in https://github.com/Naruno/Naruno/pull/1199
* lib: Added transactions to performance analyzers by @onuratakan in https://github.com/Naruno/Naruno/pull/1201
* lib: Seperating normal block and hard block performance analyzers by @onuratakan in https://github.com/Naruno/Naruno/pull/1207


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.32.1-alpha...v0.33.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
