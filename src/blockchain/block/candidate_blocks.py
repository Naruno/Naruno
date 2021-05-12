#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os
import pickle

from lib.config_system import get_config

from config import *


class candidate_block:
    def __init__(self):

        self.candidate_blocks = []
        self.candidate_block_hashes = []

    def save_candidate_blocks(self):

        os.chdir(get_config()["main_folder"])
        with open(TEMP_CANDIDATE_BLOCKS_PATH, 'wb') as block_file:
            pickle.dump(self, block_file, protocol=2)


def get_candidate_block():
    try:
        os.chdir(get_config()["main_folder"])
        with open(TEMP_CANDIDATE_BLOCKS_PATH, 'rb') as block_file:
            return pickle.load(block_file)
    except FileNotFoundError:
        return candidate_block()