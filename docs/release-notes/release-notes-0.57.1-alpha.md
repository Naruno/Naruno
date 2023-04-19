---
title: 0.57.1-alpha
parent: Release Notes
nav_order: 132
---

# 0.57.1-alpha Release Notes

This path, v0.57.1-alpha, includes changes to both the apps and lib sections. Checker function logging has been added and explained, as well as tests added, in the apps section. Additionally, the clear_logs function has been fixed for win32 in the lib section. 

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
Two changes have been made in the blockchain category. First, an automatic log cleaning feature has been added for block number changes. Second, a new element called use_full_block has been added to control the filled blocks.

## Apps
The checker function has undergone changes with the addition of logging and tests while being explained by @onuratakan in https://github.com/Naruno/Naruno/pull/1597.

## Lib
The win32 version issue with clear_logs has been resolved by @onuratakan in https://github.com/Naruno/Naruno/pull/1598.

# 0.57.1-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Checker function logged, added tests and explained by @onuratakan in https://github.com/Naruno/Naruno/pull/1597
### Lib
* lib: Fixed clear_logs for win32 by @onuratakan in https://github.com/Naruno/Naruno/pull/1598


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.57.0-alpha...v0.57.1-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
