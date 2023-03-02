---
title: 0.15.0-alpha
parent: Release Notes
nav_order: 32
---

# 0.15.0-alpha Release Notes

This path fix the requirements getting on the setups.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

## waitress

bump waitress from 2.0.0 to 2.1.1

# Notable changes

## Logging

Added logging system and log folder structure.

## Debugging

Added some other information to status function response.

## Auto-Builders

Added some time sleeps, so tests are more stable now.

## Block

Added hash of green paper to first block previous hash.

## Connection

Maded many improvements on node system.

## Package

Removed main pypi package from api and gui pypi package.

## Documentation

Configured the GitHub autmatic release note generator with release.yml.

## GitHub Workflows

Merged the test workflows in one workflow. Adding security scanner workflows and logs as artifacts.

## Tests

The docker based functional test moved to local based functional test
and moved the functional and unit tests under a folder named tests.

# 0.15.0-alpha change log

### API

- build(deps): bump waitress from 2.0.0 to 2.1.1 in /requirements by @dependabot in https://github.com/Naruno/Naruno/pull/353

### APP

- Removed the apps_starter and app class by @onuratakan in https://github.com/Naruno/Naruno/pull/360

### Auto-Builders

- Added some time sleeps by @onuratakan in https://github.com/Naruno/Naruno/pull/391

### Block

- block: Added green paper hash by @onuratakan in https://github.com/Naruno/Naruno/pull/368

### Connection

- 347 improvements for node modules by @onuratakan in https://github.com/Naruno/Naruno/pull/354

### Package

- 363 removing the main package from api and gui packege requirements by @onuratakan in https://github.com/Naruno/Naruno/pull/364
- readme: Added PyPI dowloads by @onuratakan in https://github.com/Naruno/Naruno/pull/393

### Documentation

- Create release.yml by @onuratakan in https://github.com/Naruno/Naruno/pull/396

### Tests

- 342 merging the test workflows in one workflow by @onuratakan in https://github.com/Naruno/Naruno/pull/362
- 359 rename and moving for testunit test and functional test by @onuratakan in https://github.com/Naruno/Naruno/pull/365
- 370 moving to the local based functional tests by @onuratakan in https://github.com/Naruno/Naruno/pull/375

### GitHub

- Delete issue-branch.yml by @onuratakan in https://github.com/Naruno/Naruno/pull/352
- 372 adding log files as artifacts to the actions by @onuratakan in https://github.com/Naruno/Naruno/pull/376
- 379 adding security scanner workflows by @onuratakan in https://github.com/Naruno/Naruno/pull/380

### Logging

- 349 adding log system by @onuratakan in https://github.com/Naruno/Naruno/pull/373

### Debugging

- status: Lots of status information added by @onuratakan in https://github.com/Naruno/Naruno/pull/377

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- @dependabot
