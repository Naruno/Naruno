---
title: 0.52.6-alpha
parent: Release Notes
nav_order: 111
---

# 0.52.6-alpha Release Notes

The latest path of Naruno, v0.52.6-alpha, includes a fix for missed transactions and multiple threads caching problem.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## App
Cache operations are disabled for checker for preventing leaks in multiple threads.

## Blockchain
Increased transaction delay to a suitable value for preventing missed transactions.

# 0.52.6-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Cache operations are disabled for checker for preventing leaks in multiple threads by @onuratakan in https://github.com/Naruno/Naruno/pull/1543
### Blockchain
* blockchain: Increased transaction delay to a suitable value for preventing missed transactions by @onuratakan in https://github.com/Naruno/Naruno/pull/1542


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.52.5-alpha...v0.52.6-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
