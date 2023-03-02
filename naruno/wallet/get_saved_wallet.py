#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from naruno.config import *
from naruno.lib.config_system import get_config


def get_saved_wallet():

    os.chdir(get_config()["main_folder"])

    if not os.path.exists(WALLETS_PATH):
        return {}

    with open(WALLETS_PATH, "r") as wallet_list_file:
        return json.load(wallet_list_file)
