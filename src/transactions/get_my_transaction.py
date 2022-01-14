#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import pickle
import os

from lib.config_system import get_config
from config import MY_TRANSACTION_PATH



def GetMyTransaction():
    """
    Returns the transaction db.
    """

    os.chdir(get_config()["main_folder"])

    if not os.path.exists(MY_TRANSACTION_PATH):
        return []

    
    with open(MY_TRANSACTION_PATH, "rb") as my_transaction_file:
        obj = pickle.load(my_transaction_file)      
        return obj
