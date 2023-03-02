---
title: 0.4.2-alpha
parent: Release Notes
nav_order: 8
---

# 0.4.2-alpha Release Notes

This patch includes some block time improvements.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Temporary Or Permanent Control For Block Time Increase Or Decrease

Now, before increasing or decreasing the block time, the temporality
of the situation is checked, thus providing a more stable and accurate
block time.

# 0.4.2-alpha change log

### Block

- Added some element to the class for determination the block time increase or decrease decision
- Removed increasing block time even if the block closes on correct time
- Added mechanism to detect if status is temporary or permanent before block time is increased or decreased

### Readme

- Changed the version number to "0.4.2-alpha"

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
