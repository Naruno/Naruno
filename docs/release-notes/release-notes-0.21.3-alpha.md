---
title: 0.21.3-alpha
parent: Release Notes
nav_order: 47
---

# 0.21.3-alpha Release Notes

With this path we fix the stability problem after
0.21.0-alpha version with reverting some updates.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

### Block

We removed the gap of block time for stability. (Decided after tests)

### Connection

We removed the check point that control taken candidate block and block
hash for stability. (Decided after tests)

### Tests

We added a workflow_dispatch trigger ability to stability_tests for more
testing and research.

# 0.21.3-alpha change log

### Block

- block: Removed gap of block time by @onuratakan in https://github.com/Naruno/Naruno/pull/480

### Connection

- node: Removed check point that control taken candidate block and block hash by @onuratakan in https://github.com/Naruno/Naruno/pull/477

### Tests

- github: Added workflow_dispatch to stability tests by @onuratakan in https://github.com/Naruno/Naruno/pull/475

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
