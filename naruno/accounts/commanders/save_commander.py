#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os

from naruno.config import COMMANDERS_PATH
from naruno.lib.config_system import get_config
from naruno.lib.kot import KOT

commanders_db = KOT("commanders", folder=get_config()["main_folder"] + "/db")


def SaveCommander(commander):
    commanders_db.set(commander, True)
