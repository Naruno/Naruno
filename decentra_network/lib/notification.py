#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from plyer import notification as plyer_notification
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger


logger = get_logger("LIB")

def notification(title, message):
    logger.info("Notification system is started")
    logger.debug(f"title: {title}")
    logger.debug(f"message: {message}")
    os.chdir(get_config()["main_folder"])
    icon = "/gui_lib/images/logo.ico"
    logger.debug(f"icon: {icon}")
    plyer_notification.notify(title=title, message=message, app_icon=icon)

