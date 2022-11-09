#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from threading import Thread

import copy

from decentra_network.lib.log import get_logger

logger = get_logger("APP")


class app(Thread):
    """
    It initiates the start functions of the applications in parallel
    from the main process.
    """

    def __init__(self, import_command, func, block):
        Thread.__init__(self)
        self.import_command = import_command
        self.func = func
        self.block = block

    def run(self):
        """
        Run the application.
        """
        exec(self.import_command)
        # lgtm [py/unused-loop-variable]
        protected_list = copy.copy(self.block.validating_list)
        for trans in protected_list:
            logger.debug(f"Application triggering for tx {trans.__dict__}")
            exec(self.func)
