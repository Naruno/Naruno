#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import os
import shutil
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from naruno.lib.config_system import get_config, save_config
from naruno.lib.log import get_logger
from naruno.lib.settings_system import save_settings, temp_json, the_settings
from naruno.config import WALLETS_PATH
from naruno.wallet.save_wallet_list import save_wallet_list

logger = get_logger("LIB")


def naruno_import(export_location: str) -> None:
    """
    Extract a ZIP archive to the `db` folder in the main directory of the application.

    Args:
        export_location: The location of the ZIP archive to be extracted.
    """
    logger.info("Import system is started")
    backup_config = copy.copy(get_config())
    main_folder = backup_config["main_folder"]
    target_location = f"{main_folder}/db/"
    logger.debug(f"export_location: {export_location}")
    logger.debug(f"target_location: {target_location}")
    shutil.unpack_archive(export_location, target_location)

    save_config(backup_config)

    after_backup_settings = the_settings()
    for element in temp_json:
        if element not in after_backup_settings:
            after_backup_settings[element] = temp_json[element]

    save_settings(after_backup_settings)


    #Wallets before KOT
    old_wallet = os.path.join(main_folder, WALLETS_PATH)
    if os.path.exists(old_wallet):
        with open(old_wallet, "r") as wallet_list_file:
            wallets = json.load(wallet_list_file)
            save_wallet_list(wallets)


    logger.info("Import completed")
