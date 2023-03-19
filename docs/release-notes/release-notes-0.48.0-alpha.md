---
title: 0.48.0-alpha
parent: Release Notes
nav_order: 96
---

# 0.48.0-alpha Release Notes

Naruno version v0.48.0-alpha brings some notable changes to the Apps, Docs, and Lib categories. `Embedded Apps` have been deprecated, and new features like `send forcer system`, `automatic splitting for big datas`, and contextlib suppress have been added to the Apps category. A new section has been added to the Docs category for `running Web3_App.py` in baklava testnet, and the Lib category has a new feature called `safe main folder` system for backup importing.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Naruno/Naruno/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
In this version update of Naruno, there have been several changes made to the apps category. Firstly, the `Embedded Apps` feature has been deprecated by @onuratakan in pull request #1512. Secondly, two new features have been added: a `send forcer system` for multiple sending at the same time, and an `automatic splitting for big datas` feature for sending big datas. These features were added in pull requests #1513 and #1514, respectively. Additionally, the contextlib suppress has also been added to prevent errors caused by the `inspect` module. This feature was added in pull request #1515.

## Docs
The docs category has been updated in this version of Naruno. A new section has been added for `running the Web3_App.py` in baklava testnet document. This change was made by @onuratakan in pull request #1511.

## Lib
The lib category has been updated in this version of Naruno. A new feature has been added which is the `safe main folder system` for backup importing. This feature was added by @onuratakan in pull request #1516.

# 0.48.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Deprecated Embedded Apps by @onuratakan in https://github.com/Naruno/Naruno/pull/1512
* apps: Added send forcer system for multiple sending in same times. (tx sequencer) by @onuratakan in https://github.com/Naruno/Naruno/pull/1513
* apps: Added automatic splitting for big datas by @onuratakan in https://github.com/Naruno/Naruno/pull/1514
* apps: Added contextlib suppress for preventing errors that caused from inspect module by @onuratakan in https://github.com/Naruno/Naruno/pull/1515
### Docs
* docs: Added a section for running the Web3_App.py in baklava testnet document by @onuratakan in https://github.com/Naruno/Naruno/pull/1511
### Lib
* lib: Added safe main folder system for backup importing by @onuratakan in https://github.com/Naruno/Naruno/pull/1516


**Full Changelog**: https://github.com/Naruno/Naruno/compare/v0.47.0-alpha...v0.48.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
