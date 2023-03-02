---
title: 0.5.0-alpha
parent: Release Notes
nav_order: 13
---

# 0.5.0-alpha Release Notes

This minor release includes several new features and major/minor fixes.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## New Block Time Optimizer

The old one was causing some issues and sync errors, so we redesigned and implemented the block time optimizer.

## New Test Environments

Systems prepared for the creation of test environments.

## New CLI Docker

Added cli docker.

# 0.5.0-alpha change log

### Block Time Optimizer

- The old block time optimizer has been removed
- Fixed the mechanism that calculates the accuracy of the block time
- A more stable and round-based accelerator has been added

### New Test Environments

- functional_test folder created
- Added docker based constructor and autotest to test environments/docker folder
- Added local constructor and autotest to test environments/local folder

### Docker

- Added cli docker

### 0.4.6-alpha Release Note

- Some fixes for round name

### Readme

- Changed the version number to "0.5.0-alpha"

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
