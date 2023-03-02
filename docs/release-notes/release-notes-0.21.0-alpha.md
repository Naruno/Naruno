---
title: 0.21.0-alpha
parent: Release Notes
nav_order: 44
---

# 0.21.0-alpha Release Notes

With this minor release we optimize many systems and added new functionalities.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

### Auto-Builders

With this release we added a functionality to connect different nodes in
different circles randomly.

### Block

With this release we clean the elements of block time optimizer.

### Connection

We added a check point to the candidate block and block hash gathering
process for less calculation.

### Documentation

We added a action for creating video with gource with release publishing.

### Tests

We optimized the functional tests for new block time and stability.

### Status

With this release we removed block time based status report.

# 0.21.0-alpha change log

### Auto-Builders

- auto_builders: Added randomly connect circle node to another circle node by @onuratakan in https://github.com/Naruno/Naruno/pull/464

### Block

- block: Removed unused elements by @onuratakan in https://github.com/Naruno/Naruno/pull/454

### Connection

- node: Added a check point for taken candidate block and hash by @onuratakan in https://github.com/Naruno/Naruno/pull/451

### Documentation

- github: Added Gource actions by @onuratakan in https://github.com/Naruno/Naruno/pull/463

### Tests

- tests: Increased the functional tests time sleeps for new block time by @onuratakan in https://github.com/Naruno/Naruno/pull/458
- tests: Optimized and fixed functional tests by @onuratakan in https://github.com/Naruno/Naruno/pull/461

### Status

- status: Removed time difference based status value by @onuratakan in https://github.com/Naruno/Naruno/pull/452

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
