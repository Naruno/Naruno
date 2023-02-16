---
title: 0.44.0-alpha
parent: Release Notes
nav_order: 82
---

# 0.44.0-alpha Release Notes

The Decentra-Network has released a new version, v0.44.0-alpha, with several changes across different categories. In the Apps category, an integration system has been added, while in the Blockchain category, start_time edits for gap blocks have been removed. The Consensus category has seen the hard block wait moved to the end of calculation, and the consensus_trigger and same level systems have been made clearer. The Packages category has been fixed for orientation setting for new versions of Buildozer. The GUI category has also seen several updates, including the addition of copy transaction signature, a main app variable, and a custom splash screen, as well as the removal of the title bar and the addition of a close button to the navbar with a popup.

Please report bugs using the issue tracker at GitHub:

<https://github.com/Decentra-Network/Decentra-Network/issues>

# Compatibility

There have been no compatibility changes.

# Notable changes

## Apps
The latest update has added the apps.remote_app.Integration system, which enables remote integration of apps.

## Blockchain
In this update, the start_time edits for gap blocks in sync have been removed.

## Consensus
The hard block wait has been moved to the end of calculation to reduce complexity and increase clarity of consensus_trigger and same level systems.

## Packages
An orientation setting for the new version of buildozer has been fixed in this release.

## GUI
The GUI has received several updates, including the ability to copy transaction signature from the transaction history section, a new main app variable, and the use of global font_path from App. Additionally, a popup class has been added, the title bar has been removed and a close button has been added to the navbar with popup. Furthermore, a custom splash screen has been introduced in this update


# 0.44.0-alpha change log

<!-- Release notes generated using configuration in .github/release.yml at master -->

## What's Changed
### Apps
* apps: Added apps.remote_app.Integration system by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1457
### Blockchain
* blockchain: Removed start_time edits for gap blocks in sync by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1439
### Consensus
* consensus: Moved the hard block wait to end of calculation by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1438
* consensus: Reduced complexity and increasing clarity of consensus_trigger and same level systems by @deyzir in https://github.com/Decentra-Network/Decentra-Network/pull/1442
### Packages
* packages: Fixed orientation setting for new version of buildozer by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1441
### GUI
* gui: Added copy transaction signature from transaction history section by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1443
* gui: Added a main app variable by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1453
* gui: Added using global font_path from App by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1454
* gui: Added popup class by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1455
* gui: Removed title bar and added close button to navbar with popup by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1462
* gui: Added custom splash screen by @onuratakan in https://github.com/Decentra-Network/Decentra-Network/pull/1463


**Full Changelog**: https://github.com/Decentra-Network/Decentra-Network/compare/v0.43.0-alpha...v0.44.0-alpha

# Credits

Thanks to everyone who directly contributed to this release:

- Onur Atakan ULUSOY
- Sami BARTU
