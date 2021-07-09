---
title: 0.4.2-alpha
parent: Release Notes
nav_order: 6
---

0.4.2-alpha Release Notes
====================

This patch changes the node approach and adds some features.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/Decentra-Network/Decentra-Network/issues>

Compatibility
==============

There have been no compatibility changes.

Notable changes
===============

## Only UNL Node Connection

Now the software will only accept UNL nodes' requests to connect, 
this will make a huge contribution to security.

0.4.2-alpha change log
=================

### Block
- Added some element to the class for determination the block time increase or decrease decision
- Removed increasing block time even if the block closes on correct time
- Added mechanism to detect if status is temporary or permanent before block time is increased or decreased

### Readme
- Changed the version number to "0.4.2-alpha"

Credits
=======

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
