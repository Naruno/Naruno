---
title: 0.55.0-alpha
parent: Release Notes
nav_order: 122
---

# 0.55.0-alpha Release Notes

Naruno's latest minor release, v0.55.0-alpha, brings some important changes to its apps, auto-builders, and lib. The release notes indicate that a new fault tolerance feature has been added to the apps for sending, and a try-except has been included to handle network issues during integration. The auto-builders feature has been updated to fix a bug related to the test mode parameter. Additionally, the lib has undergone changes, with caching and a system to prevent multiple status calls being added, along with a fix system for broken status processes.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
The latest release of Naruno has made some changes to its apps. The release notes indicate that fault tolerance has been added for sending, and a try-except has been included to handle situations when the network is not active during integration. These changes were made by @onuratakan in pull requests #1577 and #1578.

## Auto-Builders
The release notes also mention changes to the auto-builders feature. A bug related to test mode parameters has been fixed by @onuratakan in pull request #1579.

## Lib
The library of Naruno has undergone some changes as well. The release notes indicate that caching has been added for status, and a system has been implemented to prevent multiple status calls. Additionally, a fix system for broken status processes has also been added. These changes were made by @onuratakan in pull requests #1574, #1575, and #1576.


# 0.55.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Added fault tolerance for sending by @onuratakan in https://github.com/Naruno/Naruno/pull/1577
* apps: Added a try except for not active network situations in starting integration by @onuratakan in https://github.com/Naruno/Naruno/pull/1578
### Auto-Builders
* auto_builders: Fixed test mode bug with test_mode parameter by @onuratakan in https://github.com/Naruno/Naruno/pull/1579
### Lib
* lib: Added caching for status by @onuratakan in https://github.com/Naruno/Naruno/pull/1574
* lib: Added a system for preventing the multiple status call by @onuratakan in https://github.com/Naruno/Naruno/pull/1575
* lib: Added a fix system for broken status procces by @onuratakan in https://github.com/Naruno/Naruno/pull/1576


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.54.2-alpha...v0.55.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
