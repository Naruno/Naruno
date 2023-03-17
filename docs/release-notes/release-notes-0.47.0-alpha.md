---
title: 0.47.0-alpha
parent: Release Notes
nav_order: 95
---

# 0.47.0-alpha Release Notes

This minor release brings several changes to the apps, blockchain, and api modules. The apps module now includes an automatic API start feature, the blockchain module has been modified to prevent the baklava mode loop problem caused by getting balance, and the api module's request loggers have been changed to debug logs.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
The latest update to the apps module now includes automatic API start, thanks to the contribution by @onuratakan. This feature can be found in the latest pull request available at https://github.com/Naruno/Naruno/pull/1509.

## Blockchain
In this update, the blockchain module has been modified to change the `SaveBlock` baklava settings to another setting that prevents the baklava mode loop problem caused by getting balance. This update was also contributed by @onuratakan and can be viewed in the pull request at https://github.com/Naruno/Naruno/pull/1508.

## API
The api module has undergone changes in this update. The request loggers have now been changed to debug logs, thanks to the contribution by @onuratakan. You can view the full details of this update in the pull request at https://github.com/Naruno/Naruno/pull/1510.

# 0.47.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Added automatic api start by @onuratakan in https://github.com/Naruno/Naruno/pull/1509
### Blockchain
* blockchain: Changed saveblock baklava settings with another settings for preventing baklava mode loop problem caused from getting balance by @onuratakan in https://github.com/Naruno/Naruno/pull/1508
### API
* api: Changed request loggers to debug logs by @onuratakan in https://github.com/Naruno/Naruno/pull/1510


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.46.5-alpha...v0.47.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
