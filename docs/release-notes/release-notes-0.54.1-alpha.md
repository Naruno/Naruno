---
title: 0.54.1-alpha
parent: Release Notes
nav_order: 120
---

# 0.54.1-alpha Release Notes

With this path we fix the bug in sequence number calculation for integration based sequance number evaluation.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
With this path we connect the sequence number calculation to the api.

## API
We fix the sequence number calculation by added block parameter as default for `/sequence/get/` api.


# 0.54.1-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Sequance number calculation moved to api by @onuratakan in https://github.com/Naruno/Naruno/pull/1565
### API
* api: `/sequence/get/` api fixed by @onuratakan in https://github.com/Naruno/Naruno/pull/1565

**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.54.0-alpha...v0.54.1-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
