---
title: 0.4.1-alpha
parent: Release Notes
nav_order: 7
---

# 0.4.1-alpha Release Notes

This patch changes the node approach and adds some features.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Only UNL Node Connection

Now the software will only accept UNL nodes' requests to connect,
this will make a huge contribution to security.

# 0.4.1-alpha change log

### CLI

- Added the print the id function ("ndid")
- Removed get full node list and connect to the main network functions and menus
- Removed unused debug settings for nodes

### GUI

- Added the copy the id function (in the node page)
- Removed get full node list and connect to the main network functions and buttons
- Removed unused debug settings for nodes

### Node

- Removed get_node_list.py
- Removed get full node list and connect to the main network
- Added connection controller for check is UNL

### Node Connection

- Added ndid function for returning the ID

### UNL

- Removed unused control mechanism
- Some fixes for removed unused control mechanism

### Test

- Some fixes for node testing

### Readme

- Changed the version number to "0.4.1-alpha"

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
