0.3.1-alpha Release Notes
====================

This patch contains many improvements to the GUI.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/Decentra-Network/Decentra-Network/issues>

Compatibility
==============

There have been no compatibility changes.

Notable changes
===============

## GUI Improvements

You can now set a separate password for each wallet, 
which you will need to enter when creating a wallet 
or when a privatekey is required.

* The first wallet cannot be encrypted as it is used for your connection to the network in the background, but you will still be prompted for a password.

0.3.1-alpha change log
=================

### Requirements
- Added kivymd_extensions.sweetalert==0.1.5

### GUI
- Added minumumand default width-height
- Column amount reduced from 3 to 2 on the node and wallet page
- SweetAlert is used instead of toast
- SweetAlert is used instead of Dialog
- Responsive has been added to Wallet, operations and node pages
- Added kivymd widgets instead of kivy widgets in settings and welcome pages
- Welcome screen has been migrated from gridlayout to boxlayout

Credits
=======

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
