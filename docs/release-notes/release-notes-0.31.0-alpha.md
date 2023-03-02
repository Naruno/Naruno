---
title: 0.31.0-alpha
parent: Release Notes
nav_order: 63
---

# 0.31.0-alpha Release Notes

With this minor version we deprecated the old `/export/transactions/json` API and we are fix some problems on docs.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## API

With this release we deprecated the old `/export/transactions/json` API. And we prepare the systems for new `/transactions/` APIs.

## Docs
We are fix the building app link in remote and embedded app documents. And we are fix indention problems of remote app full code. Lastly we are update the remote docs for new `/transactions/` APIs.

## GitHub

We added a workflow named `release.yml` for creating release from pushing tags.

# 0.31.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### API
* api: Deprecated old incompatible `/export/transactions/json` API by @onuratakan in https://github.com/Naruno/Naruno/pull/1159
### Docs
* docs: Some fixes for remote app document by @onuratakan in https://github.com/Naruno/Naruno/pull/1160
* docs: Fixed building a test network link of remote app document by @onuratakan in https://github.com/Naruno/Naruno/pull/1161
### GitHub
* github: Added automatic release generator by pushing tag by @onuratakan in https://github.com/Naruno/Naruno/pull/1158


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.30.3-alpha...v0.31.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
