#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
from hashlib import sha256

from naruno.config import COMMANDERS_PATH
from naruno.lib.config_system import get_config


def SaveCommander(commander):
    the_path = COMMANDERS_PATH + commander
    os.chdir(get_config()["main_folder"])
    with open(the_path, "w") as my_transaction_file:
        my_transaction_file.write("1")
