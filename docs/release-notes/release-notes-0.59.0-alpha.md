---
title: 0.59.0-alpha
parent: Release Notes
nav_order: 137
---

# 0.59.0-alpha Release Notes

This release introduces several updates across different modules and components of the system. Changes include additions to the Blockchain module, enhancements to the CLI with new sign and verify functions, updates to the documentation with contributor information and a new document for a docker-based automatic test network, the addition of unit tests for the Integration class, improvements to the GitHub release process, updates to the GUI layout of the settings page, the addition of backup system functions in the GUI, and a change in the lib module for better error handling.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Blockchain
Added different start times for shares and added docstring for shares.

## CLI
Added sign function to CLI argument and added verify function to CLI argument.

## Docs
Added contributors to readme and added docker based automatic test network doc.

## Tests
Added some unit tests for Integration class.

## GitHub
Added a concurrency group value for dividing releases from pushes.

## GUI
Fixed layout of settings page, added backup system functions, and added special folder for android in signed data saving.

## Lib
Changed "None" return to "Password is not true".

# 0.59.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Blockchain
* blockchain: Added different start times for shares by @onuratakan in https://github.com/Naruno/Naruno/pull/1637
* blockchain: Added docstring for shares by @onuratakan in https://github.com/Naruno/Naruno/pull/1640
### CLI
* cli: Added sign function to CLI argument by @onuratakan in https://github.com/Naruno/Naruno/pull/1645
* cli: Added verify function to CLI argument by @onuratakan in https://github.com/Naruno/Naruno/pull/1646
### Docs
* docs: Added contributors to readme by @onuratakan in https://github.com/Naruno/Naruno/pull/1638
* docs: Added docker based automatic test network doc by @onuratakan in https://github.com/Naruno/Naruno/pull/1642
### Tests
* tests: Added some unit tests for Integration class by @onuratakan in https://github.com/Naruno/Naruno/pull/1649
### GitHub
* github: Added a concurrency group value for dividing releases from pushes by @onuratakan in https://github.com/Naruno/Naruno/pull/1634
### GUI
* gui: Fixed layout of settings page by @onuratakan in https://github.com/Naruno/Naruno/pull/1652
* gui: Added backup system functions by @onuratakan in https://github.com/Naruno/Naruno/pull/1650
* gui: Added special folder for android in signed data saving by @onuratakan in https://github.com/Naruno/Naruno/pull/1654
### Lib
* lib: Changed "None" return to "Password is not true" by @onuratakan in https://github.com/Naruno/Naruno/pull/1648


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.58.1-alpha...v0.59.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
