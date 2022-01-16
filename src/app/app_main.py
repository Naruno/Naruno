#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os

from threading import Thread

from lib.mixlib import dprint


class app(Thread):
    """
    It initiates the start functions of the applications in parallel
    from the main process.
    """

    def __init__(self, import_command, func):
        Thread.__init__(self)
        self.import_command = import_command
        self.func = func

    def run(self):
        """
        Run the application.
        """

        exec(self.import_command)
        exec(self.func)
        dprint("App is started")


def apps_starter():
    """
    Finds applications and sends them to the app().
    """

    port = 79
    for folder_entry in os.scandir("app"):
        if (
            ".md" not in folder_entry.name
            and "__" not in folder_entry.name
            and "app_main" not in folder_entry.name
        ):
            for entry in os.scandir("app/" + folder_entry.name):
                if entry.is_file():
                    if (
                        entry.name[0] != "_"
                        and ".py" in entry.name
                        and "_main" in entry.name
                    ):
                        port += 1
                        import_command = f"from app.{folder_entry.name}.{entry.name.replace('.py','')} import {entry.name.replace('.py','')}_run"
                        tx_command = f"{entry.name.replace('.py','')}_run({port})"

                        exec(import_command)

                        x = app(import_command, tx_command)
                        x.start()


def app_tigger(block):
    """
    Notifies applications of validated transactions after
    the block is validated.
    """

    for folder_entry in os.scandir("app"):
        if (
            ".md" not in folder_entry.name
            and "__" not in folder_entry.name
            and "app_main" not in folder_entry.name
        ):
            for entry in os.scandir("app/" + folder_entry.name):
                if entry.is_file():
                    if (
                        entry.name[0] != "_"
                        and ".py" in entry.name
                        and "_main" in entry.name
                    ):
                        for (
                            trans
                        ) in block.validating_list:  # lgtm [py/unused-loop-variable]
                            import_command = f"from app.{folder_entry.name}.{entry.name.replace('.py','')} import {entry.name.replace('.py','')}_tx"
                            tx_command = f"{entry.name.replace('.py','')}_tx(trans)"
                            exec(import_command)
                            exec(tx_command)
