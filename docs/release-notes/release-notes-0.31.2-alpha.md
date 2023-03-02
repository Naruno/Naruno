---
title: 0.31.2-alpha
parent: Release Notes
nav_order: 65
---

# 0.31.2-alpha Release Notes

With this path we fix the part_amount approach and added infrustracture for the transactions proofs. Also we are maded some additions and edits in some other systems.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
We are added the part_amount approach to the blockchain. This approach is for the transactions proofs. Also we are added blockchain db saving condiditions by this update.

## Consensus
We are set the round time checks to bigger or equal from just bigger.

## Packages
With this path we added decentra_network_api package to decentra_network_tests as a requirement.

## Docs

Added block concept documents and frequently asked questions also we added website link to navbar.

# 0.31.2-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Blockchain
* blockchain: Changed blockchain db saving condition to transaction from us or to us by @onuratakan in https://github.com/Naruno/Naruno/pull/1173
* blockhain: Fixed all of part_amount system by @onuratakan in https://github.com/Naruno/Naruno/pull/1174
* blockchain: Added saving the whole of blockshash list when a block that have a transaction releated to us by @onuratakan in https://github.com/Naruno/Naruno/pull/1175
### Consensus
* consensus: Fixed and cleaned round time calculators by @onuratakan in https://github.com/Naruno/Naruno/pull/1162
### Packages
* packages: Added decentra_network_api as an requirement to tests by @onuratakan in https://github.com/Naruno/Naruno/pull/1169
### Docs
* docs: Added blockchain concept document by @onuratakan in https://github.com/Naruno/Naruno/pull/1163
* docs: Added website link by @onuratakan in https://github.com/Naruno/Naruno/pull/1164
* docs: Added Frequently Asked Questions by @onuratakan in https://github.com/Naruno/Naruno/pull/1165


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.31.1-alpha...v0.31.2-alpha


# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
