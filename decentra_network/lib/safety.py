#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from decentra_network.lib.log import get_logger
from decentra_network.lib.settings_system import the_settings

logger = get_logger("Safety")


def safety_check(interface=None, timeout=None):
    logger.info("Checking safety")
    try:
        from pywall import pywall

        the_pywall = pywall()
        if interface is not None:
            the_pywall.iface = interface
        if timeout is not None:
            the_pywall.timeout = timeout
        control = the_pywall.control()
        if control is not None:
            if control:
                logger.info("NOT Safe")
                exit()
            else:
                logger.info("Safe")
        elif the_settings()["debug_mode"]:
            logger.info("Control check is none but passing because of debug mode")
        else:
            logger.info("NOT Safe (Control check is None)")
            exit()
    except ImportError:
        logger.info("Passing safety check (no pywall)")
