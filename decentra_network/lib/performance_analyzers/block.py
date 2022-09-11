#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import hashlib
import os
import sys
import time
from cgitb import reset

from speed_calculator import calculate

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from decentra_network.accounts.account import Account
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.blocks_hash import (GetBlockshash,
                                                           GetBlockshash_part,
                                                           SaveBlockshash,
                                                           SaveBlockshash_part)
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock


class Block_IO_Performance_Analyzer:
    """
    This class is used to analyze the performance of GetBlock
    """

    def __init__(self):
        self.block = Block("test")
        self.block.first_time = False

        self.block.hash = hashlib.sha256("test".encode()).hexdigest()
        self.block.round_2_starting_time = time.time()
        self.block.validated_time = time.time()

    def analyze(self) -> float:
        """
        This function is used to analyze the performance of GetBlock
        """

        result = (
            calculate(self.save_operation)[0],
            calculate(self.get_operation)[0],
            os.path.getsize("db/Block_Performance_Analyzer_block.pf") /
            1000000,
        )

        os.remove("db/Block_Performance_Analyzer_block.pf")

        return result

    def save_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """
        SaveBlock(
            self.block,
            custom_TEMP_BLOCK_PATH="db/Block_Performance_Analyzer_block.pf",
        )

    def get_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        GetBlock("db/Block_Performance_Analyzer_block.pf")


if __name__ == "__main__":
    print(Block_IO_Performance_Analyzer().analyze())
