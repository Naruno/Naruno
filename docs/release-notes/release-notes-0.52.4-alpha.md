---
title: 0.52.4-alpha
parent: Release Notes
nav_order: 109
---

# 0.52.4-alpha Release Notes

The latest path of Naruno (v0.52.4-alpha) includes a fix for preventing transaction corruptions in the application's transaction system. This fix was implemented in the Apps category, where the transaction system will now be disabled when the 'get_all' function is true.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
In this update, a fix has been implemented for preventing transaction corruptions in the application. Specifically, the transaction system will now be disabled when the 'get_all' function is true.

# 0.52.4-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Disabled my transacton system when the get_all is true for preventing my transactions corruptions by @onuratakan in https://github.com/Naruno/Naruno/pull/1540


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.52.3-alpha...v0.52.4-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
