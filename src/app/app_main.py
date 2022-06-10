#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from threading import Thread

from lib.log import get_logger

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
        for trans in self.block.validating_list:  # lgtm [py/unused-loop-variable]
            logger.debug(f"Application triggering for tx {trans.__dict__}")
            exec(self.func)




def app_tigger(block):
    """
    Notifies applications of validated transactions after
    the block is validated.
    """

    logger.info(f"Triggering applications for block {block.sequance_number}:{block.empty_block_number}")

    for folder_entry in os.scandir("app"):
        logger.debug(f"Found application {folder_entry.name}")
        if (".md" not in folder_entry.name and "__" not in folder_entry.name
                and "app_main" not in folder_entry.name):
            logger.debug(f"Starting thread for application {folder_entry.name}")
            for entry in os.scandir("app/" + folder_entry.name):
                logger.debug(f"Found entry {entry.name}")
                if entry.is_file():
                    logger.debug(f"Found file {entry.name}")
                    if (entry.name[0] != "_" and ".py" in entry.name
                            and "_main" in entry.name):
                        logger.debug(f"Starting thread for file {entry.name}")
                        import_command = f"from app.{folder_entry.name}.{entry.name.replace('.py','')} import {entry.name.replace('.py','')}_tx"
                        tx_command = f"{entry.name.replace('.py','')}_tx(trans)"
                        logger.debug(f"import command: {import_command}")
                        logger.debug(f"tx_command: {tx_command}")
                        try:
                            x = app(import_command, tx_command, block)
                            x.start()
                        except Exception as e:
                            logger.exception(e)
