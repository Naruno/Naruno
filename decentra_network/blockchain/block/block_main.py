#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import json
import os
import time

from decentra_network.accounts.account import Account
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash
from decentra_network.config import TEMP_BLOCK_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger
from decentra_network.node.unl import Unl
from decentra_network.transactions.transaction import Transaction

logger = get_logger("BLOCKCHAIN")


class Block:
    """
    Block class is most important class. It is responsible for
    resetting and saving blocks.

    You must give a creator of the block. This creator will
    own all the coins.
    """

    def __init__(
        self,
        creator,
        previous_hash="1a00d983803e3adcbda2ed40ecba828083221648a90150267d8b0fd500c59750",
    ):
        self.coin_amount = 10000000
        self.first_time = True
        self.creator = creator
        self.genesis_time = int(time.time())
        self.start_time = int(time.time())
        self.block_time = 22

        self.previous_hash = previous_hash
        self.sequence_number = 0
        self.empty_block_number = 0
        self.hard_block_number = 2
        self.gap_block_number = self.hard_block_number + 2

        self.validating_list = []
        self.transaction_fee = 0.02
        self.default_transaction_fee = 0.02
        self.default_optimum_transaction_number = 200
        self.default_increase_of_fee = 0.01
        self.transaction_delay_time = 60
        self.max_data_size = 1000000

        self.part_amount = 1000

        self.hash = None
        self.part_amount_cache = previous_hash

        self.max_tx_number = 2
        self.minumum_transfer_amount = 1000

        self.round_1_time = 10
        self.round_1 = False

        self.round_2_starting_time = None
        self.round_2_time = 10
        self.round_2 = False

        self.consensus_timer = 0.50

        self.validated = False
        self.validated_time = None

        self.dowload_true_block = ""
        self.sync = False

        self.shares = []
        self.fee_address = creator

    def reset_the_block(self, custom_nodes=None):
        """
        When the block is verified and if block have a transaction
        and if block have at least half of the max_tx_number transaction,it saves the block
        and makes the edits for the new block.
        """

        self.start_time = (self.genesis_time +
                           ((self.sequence_number + self.empty_block_number) *
                            self.block_time)) + self.block_time

        self.round_1 = False

        self.round_2_starting_time = None
        self.round_2 = False

        self.validated = False
        self.validated_time = None

        if len(self.validating_list) >= (self.max_tx_number / 2):
            block2 = copy.copy(self)
            # Resetting and setting the new elements.
            self.previous_hash = self.hash
            self.sequence_number = self.sequence_number + 1
            self.validating_list = []
            self.hash = None
            logger.info("New block created")
            self.sync_empty_blocks()
            logger.debug(self.__dict__)
            return [block2, self]
        else:
            logger.info(
                "New block not created because no transaction enought to create a new block"
            )
            self.sync_empty_blocks()
            return False

    def sync_empty_blocks(self):
        if not self.validated:
            first_empty_block = self.empty_block_number
            sequence_number_time = self.genesis_time + (
                (self.sequence_number) * self.block_time)
            extra = int(time.time()) - sequence_number_time
            adding = extra // self.block_time
            secondly_empty_block = adding
            if not first_empty_block > secondly_empty_block:
                self.empty_block_number = adding
            self.start_time = self.genesis_time + (
                (self.sequence_number + self.empty_block_number) *
                self.block_time)
            if self.round_1:
                self.round_2_starting_time = self.start_time + self.round_1_time

    def dump_json(self):
        """
        Dumps the block as json.
        """
        temp_block = copy.copy(self)

        temp_validating_list = [
            transaction.dump_json()
            for transaction in temp_block.validating_list
        ]

        temp_block.validating_list = temp_validating_list
        return temp_block.__dict__

    @staticmethod
    def load_json(json_string):
        temp_validating_list = [
            Transaction.load_json(tx) for tx in json_string["validating_list"]
        ]

        the_block_json = json.loads(json.dumps(json_string))
        the_block_json["validating_list"] = temp_validating_list
        the_block = Block("Decentra-Network")
        the_block.__dict__ = the_block_json

        return the_block
