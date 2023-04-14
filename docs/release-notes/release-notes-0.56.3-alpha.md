---
title: 0.56.3-alpha
parent: Release Notes
nav_order: 126
---

# 0.56.3-alpha Release Notes

The latest path of Naruno (v0.56.3-alpha) includes a new fix that resolves an issue with the send function in the network API. The update moves the try except block to the correct location to fix the problem.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## API
The latest version of Naruno (v0.56.3-alpha) includes a fix for the send function in network uses. This issue was addressed in pull request #1584, where try except was moved to resolve the problem.

# 0.56.3-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### API
* api: Fixed send api in network uses with moving try except by @onuratakan in https://github.com/Naruno/Naruno/pull/1584


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.56.2-alpha...v0.56.3-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
