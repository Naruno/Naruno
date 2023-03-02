---
title: 0.29.0-alpha
parent: Release Notes
nav_order: 57
---

# 0.29.0-alpha Release Notes

With this minor release we are introduce our new docs system. Also we changed some APIs and we fix the status bug.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Docs

All of docs system has been redesigned and written from scratch.
Now we have many new features like:

- Getting started
- Building a Test Network
- Creating a App
- References
- Concepts
  ...

## API

With this version we are decided to depreceted the same old sending transaction system APIs. And we are created a new API as `/send` this API can be used to send transactions to the network. This API is more stable and more easy to use.

## Lib

We are fix the status system status reporting system. Now we are added a disable caching system ability, and we are added to status system for true status reporting.

# 0.29.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed

### Apps

- apps: Added a test applications dedect and disable methods for real usages by @onuratakan in https://github.com/Naruno/Naruno/pull/1078

### Blockchain

- blockchain: Added no_cache option for GetBlock by @onuratakan in https://github.com/Naruno/Naruno/pull/1074

### Docs

All of docs are edited and updated.

### Library

- lib: Added cache disable ability for cache system
- lib: Added disabling caching for status function

### API

- api: Moved and sended to deprecation process `/send/coin` to `/send_old/coin`
- api: Deprecated `/send/coin-data` api
- api: Added `/send` api for all transaction sendin operations

**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.28.0-alpha...v0.29.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
