#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from plyer import notification as plyer_notification
from plyer.utils import platform

from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger

logger = get_logger("LIB")


def notification(title, message):
    logger.info("Notification system is started")
    app_name = "Decentra Network"
    timeout = 10
    logger.debug(f"app_name: {app_name}")
    logger.debug(f"timeout: {timeout}")
    logger.debug(f"title: {title}")
    logger.debug(f"message: {message}")
    main_folder = get_config()["main_folder"]
    if platform == "win":
        icon = f"{main_folder}/gui_lib/images/logo_win.ico"
    else:
        icon = f"{main_folder}/gui_lib/images/logo.png"

    logger.debug(f"icon: {icon}")
    plyer_notification.notify(
        title=title, message=message, app_icon=icon, app_name=app_name, timeout=timeout
    )
