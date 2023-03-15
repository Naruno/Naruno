#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from naruno.lib.config_system import get_config
from naruno.lib.log import get_logger
from naruno.lib.settings_system import the_settings

logger = get_logger("LIB")


def notification(title, message, raise_plyer=False):
    if the_settings()["mute_notifications"] == True:
        logger.info("Notifications are muted")
        return False

    try:
        if raise_plyer:
            raise ImportError
        else:
            None

        from plyer import notification as plyer_notification
        from plyer.utils import platform

        logger.debug("Notification system is started")
        app_name = "Naruno"
        timeout = 10
        logger.debug(f"app_name: {app_name}")
        logger.debug(f"timeout: {timeout}")
        logger.debug(f"title: {title}")
        logger.debug(f"message: {message}")
        main_folder = get_config()["main_folder"]

        icon = (f"{main_folder}/gui_lib/images/logo_win.ico" if platform
                == "win" else f"{main_folder}/gui_lib/images/logo.png")

        logger.debug(f"icon: {icon}")
        plyer_notification.notify(
            title=title,
            message=message,
            app_icon=icon,
            app_name=app_name,
            timeout=timeout,
        )
    except ImportError:
        logger.debug("Passing notification system (no plyer)")
    except NotImplementedError:
        logger.debug(
            "Passing notification system (no usable implementation found for notification)"
        )


if __name__ == "__main__":
    notification("Bahri Can", "Ergül")
