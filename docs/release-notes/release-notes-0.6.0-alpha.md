---
title: 0.6.0-alpha
parent: Release Notes
nav_order: 15
---

# 0.6.0-alpha Release Notes

This minor release includes very importand feature and additions and fixes and security patches.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## New Workflow

Added the functional test workflow

## New Docker files

Added the local builded dockerfiles for cli and api

## Worflow Improvements

Each Workflos edited for run in some stuation

## Code Quality Improvements

Edited lots of area for improvement the code quality

## New Docs

Added and edited lots of documents

## Storage Improvements

Added a rule for block saving:

- Each user should only save the block containing their transaction

## Important Fixes

- The transaction system fromUser parameter mistakes fixed

## Transaction System Vulnerability Fixes

The transaction system doublespend vulnerability fixed

## New Export Future

Now each user can export their own transactions

## Functional Test Performance Improvements

Reduced duration of function tests

# 0.6.0-alpha change log

### Consensus First Round

- Added control mechanism the same blocks in candidate blocks for loops

### Documents

- Edited the name of "apps/Definition For App" document
- Edited the all content of "getting_started/Using" document
- Added the "Google Cloud Shell Tutorials" document
- Added "API Referance" document
- Added "CLI Parameters" document

### Functional Test (old name test_environments)

- Changed the name
- Some time sleps is reduced or increased or removed for new same transaction control points
- Changed the class name in local functional test

### Core Quality

- Almost all files edited for PEP8 format

### Consensus

- Added the control mechanism for same candidate block double vote in first round

## Block

- Added mechanism for each user to save only the block containing their transaction

### Transaction

- Fixed the pubkey saving mistakes
- Added a mechanism in tx_already_got function for doublespend vulnerability
- Added a mechanism as SameTransactionGuard function for doublespend vulnerability
- Added the export as csv function
- Added a function that records all transactions of the user
- Added a trigger in createtrans function for SameTransactionGuard

### API

- Added the export the transaction api

### CLI

- Added parameter and menu for exporting the transactions

### GUI

- Added a button to operation page for exporting the transactions

### NEW Export

- Added a mechanism for obj list to csv

### Pytest.ini

- Changed the test_environments to functional_test

### Readme

- Changed the version number to "0.6.0-alpha"

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- Bahri Can Ergül
