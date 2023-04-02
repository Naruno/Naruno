---
title: 0.52.12-alpha
parent: Release Notes
nav_order: 117
---

# 0.52.12-alpha Release Notes

We are excited to announce the latest path of Naruno! This release includes some important changes to preventing errors. Specifically, we have added a minimum buffer size to prevent errors caused by bad configurations, and added naruno_api as a requirement to naruno_remote_app. These changes were contributed by @onuratakan in their pull requests. Check out the full changelog at https://github.com/Naruno/Naruno/compare/v0.52.11-alpha...v0.52.12-alpha.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Node
The latest update to Naruno now includes a new feature to prevent errors caused by bad configurations. This was accomplished by adding a minimum buffer size. Thanks to @onuratakan for contributing to this feature in https://github.com/Naruno/Naruno/pull/1555.

## Packages
In the latest version of Naruno, we have added naruno_api as a requirement to naruno_remote_app. This is a necessary update that preventing some errors. Thanks to @onuratakan for contributing to this feature in https://github.com/Naruno/Naruno/pull/1556.

# 0.52.12-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Node
* node: Added minumum buffer size for preventing errors that caused by bad configs by @onuratakan in https://github.com/Naruno/Naruno/pull/1555
### Packages
* packages: Added naruno_api as an requirement to naruno_remote_app by @onuratakan in https://github.com/Naruno/Naruno/pull/1556


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.52.11-alpha...v0.52.12-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
