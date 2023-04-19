---
title: 0.57.0-alpha
parent: Release Notes
nav_order: 131
---

# 0.57.0-alpha Release Notes

This minor release includes several changes to the blockchain and lib. The blockchain now includes automatic log cleaning for block number changes and a new use_full_block element for block filled controlling. The lib has a new log cleaner and a setting to disable log cleaning.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
Two changes have been made in the blockchain category. First, an automatic log cleaning feature has been added for block number changes. Second, a new element called use_full_block has been added to control the filled blocks.

## Lib
In the lib category, two new features have been added. The first feature is the log cleaner, and the second feature is a setting to disable the log cleaning.

Therefore, this update includes a fix to the lib category that resolves a win32-related bug.

# 0.57.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Blockchain
* blockchain: Added automatic log cleaning for block number changes by @onuratakan in https://github.com/Naruno/Naruno/pull/1594
* blockchain: Added use_full_block element for block for filled controlling by @onuratakan in https://github.com/Naruno/Naruno/pull/1596
### Lib
* lib: Added log cleaner by @onuratakan in https://github.com/Naruno/Naruno/pull/1593
* lib: Added a setting for disabling log cleaning by @onuratakan in https://github.com/Naruno/Naruno/pull/1595


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.56.7-alpha...v0.57.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
