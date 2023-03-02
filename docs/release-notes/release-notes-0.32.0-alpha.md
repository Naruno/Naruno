---
title: 0.32.0-alpha
parent: Release Notes
nav_order: 66
---

# 0.32.0-alpha Release Notes

With this minor version we are added get and check transaction proof ability to CLI and API. Also we are working on some documentation updates.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Transactions
With this minor version we added two function for the transactions proofs. One of them is for getting the transaction proof and the other one is for checking the transaction proof.

- `naruno.transactions.my_transactions.get_proof.GetProof`
- `naruno.transactions.my_transactions.check_proof.CheckProof`

## CLI
Added two new commands for the argument based CLI about the transaction proof:
- `--getproof` or `-gp`
- `--checkproof` or `-cp`

And added two menu options for the interactive CLI about the transaction proof:
- `GetProof`
- `CheckProof`

## API
Added two new endpoints for the API about the transaction proof:

- `POST /proof/get/`
- `POST /proof/check/`

## Docs
With this release we added some docs about the transaction proof and the part_amount.

# 0.32.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Transactions
* transactions: Added GetProof and CheckProof function by @onuratakan in https://github.com/Naruno/Naruno/pull/1179
### CLI
* cli: Added get and check proof ability to CLI by @onuratakan in https://github.com/Naruno/Naruno/pull/1186
### API
* api: Added get and check proof of transaction ability by @onuratakan in https://github.com/Naruno/Naruno/pull/1189
### Docs
* docs: Added proofs docs by @onuratakan in https://github.com/Naruno/Naruno/pull/1183
* docs: Added docs for part_amount system by @onuratakan in https://github.com/Naruno/Naruno/pull/1184


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.31.2-alpha...v0.32.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
