#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import os
import sys
import time

from decentra_network.config import LOGS_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.lib.settings_system import the_settings


def get_logger(name):
    logger = logging.getLogger(name)
    level = logging.DEBUG if the_settings()["debug_mode"] else logging.INFO
    logger.setLevel(level)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    # file
    main_folder = get_config()["main_folder"]
    fh = logging.FileHandler(os.path.join(main_folder, LOGS_PATH, f"{name}.log"))
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
