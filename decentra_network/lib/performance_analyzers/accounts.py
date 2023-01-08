#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

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
from decentra_network.blockchain.block.hash.accounts_hash import AccountsHash
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.lib.mix.merkle_root import MerkleTree


class Accounts_IO_Performance_Analyzer:
    """
    This class is used to analyze the performance of GetBlock
    """

    def __init__(self):
        self.block = Block("test")

        self.account = Account("test", 5000)

        self.the_account_list = []

        for i in range(self.block.coin_amount // self.block.minumum_transfer_amount):
            self.the_account_list.append(self.account)

        SaveAccounts(
            self.the_account_list,
            custom_TEMP_ACCOUNTS_PATH=
            "db/Accounts_Performance_Analyzer_accounts_2.pf",
        )

        self.getted_accounts = GetAccounts(
            "db/Accounts_Performance_Analyzer_accounts_2.pf")

    def analyze(self) -> float:
        """
        This function is used to analyze the performance of GetBlock
        """

        result = (
            calculate(self.save_operation)[0],
            calculate(self.get_operation)[0],
            os.path.getsize("db/Accounts_Performance_Analyzer_accounts.pf") /
            1000000,
        )

        os.remove("db/Accounts_Performance_Analyzer_accounts.pf")

        return result

    def save_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        SaveAccounts(
            self.the_account_list,
            custom_TEMP_ACCOUNTS_PATH=
            "db/Accounts_Performance_Analyzer_accounts.pf",
        )

        AccountsHash(self.block, self.getted_accounts)

    def get_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        GetAccounts("db/Accounts_Performance_Analyzer_accounts.pf")


if __name__ == "__main__":
    print(Accounts_IO_Performance_Analyzer().analyze())
