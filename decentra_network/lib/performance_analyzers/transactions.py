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
from decentra_network.transactions.check.check_transaction import \
    CheckTransaction
from decentra_network.transactions.transaction import Transaction


class Transactions_IO_Performance_Analyzer:
    """
    This class is used to analyze the performance of GetBlock
    """

    def __init__(self):
        self.block = Block("test")

        the_transaction_json = {
            "sequance_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        self.block = Block(the_transaction.fromUser)
        self.block.transaction_delay_time = 60
        self.block.minumum_transfer_amount = 1000

        self.the_transaction_list = [
            the_transaction for i in range(self.block.max_tx_number)
        ]

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

        for the_transaction in self.the_transaction_list:
            CheckTransaction(
                self.block,
                the_transaction,
                custom_current_time=(the_transaction.transaction_time + 5),
                custom_sequence_number=0,
                custom_balance=100000,
            )

    def get_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        GetBlock("db/Block_Performance_Analyzer_block.pf")


if __name__ == "__main__":
    print(Transactions_IO_Performance_Analyzer().analyze())
