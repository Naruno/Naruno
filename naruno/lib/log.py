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

from naruno.config import LOGS_PATH
from naruno.lib.config_system import get_config
from naruno.lib.settings_system import the_settings

global_logger = []

re# Define colors for log output
RESET_SEQ = "\033[0m"
COLORS = {
    "WARNING": "\033[33m",
    "INFO": "\033[32m",
    "DEBUG": "\033[34m",
    "CRITICAL": "\033[31m",
    "ERROR": "\033[35m",
}

class ColoredFormatter(logging.Formatter):
    """
    A formatter that adds color to log output
    """
    if sys.platform.lower() == "win32":
        os.system("")

    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            record.levelname = f"{COLORS[levelname]}{levelname}{RESET_SEQ}"
        return super().format(record)

def get_logger(name):
    logger = logging.getLogger(name)

    if not any(element == logger for element in global_logger):

        level = logging.DEBUG if the_settings()["debug_mode"] else logging.INFO
        logger.setLevel(level)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)
        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        colored_formatter = ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(colored_formatter)
        # add ch to logger
        logger.addHandler(ch)
        # file
        main_folder = get_config()["main_folder"]
        fh = logging.FileHandler(
            os.path.join(main_folder, LOGS_PATH, f"{name}.log"))
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        global_logger.append(logger)
    return logger
