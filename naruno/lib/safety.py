#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.lib.log import get_logger
from decentra_network.lib.settings_system import the_settings

logger = get_logger("Safety")


def safety_check(
    interface=None,
    timeout=None,
    exit_on_error=True,
    custom_pywall=None,
    custom_debug_mode=None,
):
    logger.info("Checking safety")
    try:
        the_import_string = "from pywall import pywall"
        pywall_class = (exec(the_import_string)
                        if custom_pywall is None else custom_pywall)
        the_pywall = pywall() if custom_pywall is None else custom_pywall()
        the_pywall.iface = the_pywall.iface if interface is None else interface
        the_pywall.timeout = the_pywall.timeout if timeout is None else timeout

        control = the_pywall.control()

        debug_mode = (the_settings()["debug_mode"]
                      if custom_debug_mode is None else custom_debug_mode)

        if control is not None:
            if control:
                logger.info("NOT Safe")
                exit() if exit_on_error else None
                return False
            else:
                logger.info("Safe")
                return True
        elif debug_mode:
            logger.info(
                "Control check is none but passing because of debug mode")
            return None
        else:
            logger.info("NOT Safe (Control check is None)")
            exit() if exit_on_error else None
            return False
    except ImportError:
        logger.info("Passing safety check (no pywall)")
        return None
