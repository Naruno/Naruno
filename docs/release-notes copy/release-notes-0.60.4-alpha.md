---
title: 0.60.4-alpha
parent: Release Notes
nav_order: 142
---

# 0.60.4-alpha Release Notes

This path fix some bugs and add some abilities.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility
Old backups are just compatible with wallet section. Other sections are not compatible with old backups.

# Notable changes

## Accounts
Fixed false balance problem from currently block included calculations.

## Apps
Removed backward support for cache for preventing bug. Moved new data log to main get function from _get function. Removed app name from action in Integration. Added transaction signature to message sent log in the Integration.

## GUI
Added android support for csv exports.

## Lib
Removed debug mode activating in the start bug. Changed checking safety logger to debug.

# 0.60.4-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Accounts
* accounts: Fixed false balance problem from currently block included calculations by @onuratakan in https://github.com/Naruno/Naruno/pull/1716
### Apps
* apps: Removed backward support for cache for preventing bug by @onuratakan in https://github.com/Naruno/Naruno/pull/1721
* apps: Moved new data log to main get function from _get function by @onuratakan in https://github.com/Naruno/Naruno/pull/1723
* apps: Removed app name from action in Integration by @onuratakan in https://github.com/Naruno/Naruno/pull/1724
* apps: Added transaction signature to message sent log in the Integration by @onuratakan in https://github.com/Naruno/Naruno/pull/1725
### CLI
* cli: Moved safety check to top by @onuratakan in https://github.com/Naruno/Naruno/pull/1715
### Tests
* tests: Fixed test_send_my_block_get_candidate_block_multiple_with_function_try by @onuratakan in https://github.com/Naruno/Naruno/pull/1711
### GUI
* gui: Added android support for csv exports by @onuratakan in https://github.com/Naruno/Naruno/pull/1713
### Lib
* lib: Removed debug mode activating in the start bug by @onuratakan in https://github.com/Naruno/Naruno/pull/1712
* lib: Changed checking safety logger to debug by @onuratakan in https://github.com/Naruno/Naruno/pull/1714
### Other Changes
* Loggers improved by @onuratakan in https://github.com/Naruno/Naruno/pull/1717


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.60.3-alpha...v0.60.4-alpha


# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
