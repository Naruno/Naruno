#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from hashlib import sha256

from naruno.config import COMMANDERS_PATH
from naruno.lib.config_system import get_config


def DeleteCommander(tx):
    os.chdir(get_config()["main_folder"])
    for entry in os.scandir(COMMANDERS_PATH):
        if tx in entry.name:
            os.remove(entry.path)
