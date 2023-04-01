---
title: 0.52.11-alpha
parent: Release Notes
nav_order: 116
---

# 0.52.11-alpha Release Notes

This path brings several changes to the Node component of the Naruno project. These changes include the addition of an empty block number for timeouts, a control point for candidate block values, separate sending for candidate block transactions, and a connection between buffer size and max_data_size and max_tx_number.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Node
In this release, several changes were made to the Node. Firstly, an empty block number was added to allow for timeouts. Secondly, a control point was added for candidate blocks values. Thirdly, the sending of candidate block transactions was separated. Finally, the buffer size was connected to max_data_size and max_tx_number.

# 0.52.11-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Node
* node: Added empty block number for making a timeout by @onuratakan in https://github.com/Naruno/Naruno/pull/1548
* node: Added a control point for candidate blocks values by @onuratakan in https://github.com/Naruno/Naruno/pull/1549
* node: Made seperated sending for candidate block txs by @onuratakan in https://github.com/Naruno/Naruno/pull/1553
* node: Connected buffer size to max_data_size and max_tx_number by @onuratakan in https://github.com/Naruno/Naruno/pull/1554


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.52.10-alpha...v0.52.11-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
