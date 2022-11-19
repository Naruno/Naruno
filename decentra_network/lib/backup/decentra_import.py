# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger

logger = get_logger("LIB")


def decentra_import(export_location):
    logger.info("Import system is started")
    main_folder = get_config()["main_folder"]
    target_location = f"{main_folder}/db/"
    logger.debug(f"export_location: {export_location}")
    logger.debug(f"target_location: {target_location}")
    shutil.unpack_archive(export_location, target_location)
    logger.info("Import complated")
