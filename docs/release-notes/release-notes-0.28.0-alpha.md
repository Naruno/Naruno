---
title: 0.28.0-alpha
parent: Release Notes
nav_order: 56
---

# 0.28.0-alpha Release Notes

With this minor release we added a caching mechanism to all of the db systems.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Lib

The functions below:

- `GetBlock`
- `GetAccounts`
- `GetBlockshash`
- `GetBlockshash_part`

has been changed to use a cache if there is a cache available.

# 0.28.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed

### Library

- lib: Added caching system by @onuratakan in https://github.com/Naruno/Naruno/pull/1062

**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.27.1-alpha...v0.28.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- Bahri Can ERGÜL
