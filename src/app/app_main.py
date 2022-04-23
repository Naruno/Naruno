#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from threading import Thread


def app_tigger(block):
    """
    Notifies applications of validated transactions after
    the block is validated.
    """

    for folder_entry in os.scandir("app"):
        if (".md" not in folder_entry.name and "__" not in folder_entry.name
                and "app_main" not in folder_entry.name):
            for entry in os.scandir("app/" + folder_entry.name):
                if entry.is_file():
                    if (entry.name[0] != "_" and ".py" in entry.name
                            and "_main" in entry.name):
                        for (
                                trans
                        ) in block.validating_list:  # lgtm [py/unused-loop-variable]
                            import_command = f"from app.{folder_entry.name}.{entry.name.replace('.py','')} import {entry.name.replace('.py','')}_tx"
                            tx_command = f"{entry.name.replace('.py','')}_tx(trans)"
                            exec(import_command)
                            exec(tx_command)
