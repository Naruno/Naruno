---
title: 0.16.1-alpha
parent: Release Notes
nav_order: 36
---

# 0.16.1-alpha Release Notes

This path includes a new way to create a new node and api.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Connection

With this path the ports setted to {8100 + n + 1} and node port setted {8010 + n + 1}.
Now we can open 98 node and 98 API ports for tests.

# 0.16.1-alpha change log

### Connection

- connection: New type for calculating port number by @onuratakan in https://github.com/Naruno/Naruno/pull/403

### Tests

Added **init**.py for test discovering.

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
