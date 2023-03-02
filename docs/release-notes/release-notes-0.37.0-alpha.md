---
title: 0.37.0-alpha
parent: Release Notes
nav_order: 74
---

# 0.37.0-alpha Release Notes

With this minor release we add a backend system for saving first blockshash part and first block to blockchain db.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
We add a condidition for first block and its blockshash part in consensus for blockchain system, with this update your node will save first states that if its in an new chain (is have first block and running ends of first blockshash part).


# 0.37.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Blockchain
* blockchain: Added saving first block and blockshash part always by @onuratakan in https://github.com/Naruno/Naruno/pull/1232


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.36.0-alpha...v0.37.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
