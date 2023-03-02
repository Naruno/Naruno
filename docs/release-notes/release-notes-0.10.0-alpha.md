---
title: 0.10.0-alpha
parent: Release Notes
nav_order: 24
---

# 0.10.0-alpha Release Notes

This minor version includes new features and lots of important fix.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps

Added a parameter as port to app main function. And some important fixes.

## Auto Builders (NEW)

Added a feature named "Auto Builders". With this feature you can
install, delete, run and build your own network easiy.

## Functional Tests

Local functinal test deprecated.

## Wallet

Added a control point for index_out_of_range error in Wallet_Import function.

## Transaction

Fixed the my transaction list bug (Fixed #220). Also some function moved.

## Docs

Some api path and description fixed and added some things for website.

# 0.10.0-alpha change log

### Apps

- Added the port variable giving to application main function.
- "App/apps" or "app.apps" fixed with "app/" and "app.".

### Readme

- Changed the "Explore the docs" link to "Explore the website".

### Auto Builders (NEW)

- Added auto builders for local and docker based installations.
- Added create delete run and start functions for auto builders.
- Some corruption of database cleanup functions fixed with auto
  builders.

### Functional Tests

- Local functional tests have been deprecated.

### Wallet

- Prevent that index_out_of_range is thrown when there is no wallet
  for Wallet_Import function.

### Transaction

- GetMyTransaction Function moved to get_my_transactions.py
- Fixed a bug in GetMyTransaction function that removed the first
  element in every call in my transactions. (Fixed #220)

### Docs

- Theme changed to light.
- Added google analytics code.
- Added favicon.
- Added cname.
- Some correction for path and description for API in api.md.

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- @cpyberry
