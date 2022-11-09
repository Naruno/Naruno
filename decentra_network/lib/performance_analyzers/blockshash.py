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

from decentra_network.blockchain.block.hash.blocks_hash import BlocksHash

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


class Blockshash_IO_Performance_Analyzer:
    """
    This class is used to analyze the performance of GetBlock
    """

    def __init__(self):
        self.block = Block("test")
        self.the_hash = hashlib.sha256("test".encode()).hexdigest()
        self.blocks_hash = [
            self.the_hash for i in range(self.block.part_amount - 1)
        ]
        self.blocks_hash.append(self.block.previous_hash)
        SaveBlockshash(
            self.blocks_hash,
            custom_TEMP_BLOCKSHASH_PATH=
            "db/Blockshash_Performance_Analyzer_blockshash.pf",
        )

    def analyze(self) -> float:
        """
        This function is used to analyze the performance of GetBlock
        """

        result = (
            calculate(self.save_operation)[0],
            calculate(self.get_operation)[0],
            os.path.getsize("db/Blockshash_Performance_Analyzer_blockshash.pf")
            / 1000000,
        )

        os.remove("db/Blockshash_Performance_Analyzer_blockshash.pf")

        return result

    def save_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        SaveBlockshash(
            self.the_hash,
            custom_TEMP_BLOCKSHASH_PATH=
            "db/Blockshash_Performance_Analyzer_blockshash.pf",
        )

        BlocksHash(self.block, [], self.blocks_hash)

    def get_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        GetBlockshash(custom_TEMP_BLOCKSHASH_PATH=
                      "db/Blockshash_Performance_Analyzer_blockshash.pf")


if __name__ == "__main__":
    print(Blockshash_IO_Performance_Analyzer().analyze())
