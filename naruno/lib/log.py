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

format = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
)


class ColoredFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    if sys.platform.lower() == "win32":
        os.system("")

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name):
    logger = logging.getLogger(name)

    if not any(element == logger for element in global_logger):
        level = logging.DEBUG if the_settings()["debug_mode"] else logging.INFO
        logger.setLevel(level)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)
        # create formatter
        formatter = logging.Formatter(format)
        colored_formatter = ColoredFormatter(format)
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


def clear_logs():
    if the_settings()["disable_log_clearing"]:
        return
    main_folder = get_config()["main_folder"]
    for file in os.listdir(os.path.join(main_folder, LOGS_PATH)):
        if file.endswith(".log"):
            open(os.path.join(main_folder, LOGS_PATH, file), "w").close()
