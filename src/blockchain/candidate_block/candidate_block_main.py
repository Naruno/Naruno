#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os
import pickle

from lib.config_system import get_config

from config import TEMP_CANDIDATE_BLOCKS_PATH


class candidate_block:
    def __init__(self,candidate_blocks=[], candidate_block_hashes=[]):

        self.candidate_blocks = candidate_blocks
        self.candidate_block_hashes = candidate_block_hashes
