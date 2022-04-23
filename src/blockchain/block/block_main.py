#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import pickle
import time

from accounts.account import Account
from accounts.get_accounts import GetAccounts
from accounts.save_accounts import save_accounts
from app.app_main import app_tigger
from blockchain.block.blocks_hash import GetBlockshash
from blockchain.block.blocks_hash import SaveBlockshash
from blockchain.block.blocks_hash import SaveBlockshash_part
from blockchain.block.save_block_to_blockchain_db import \
    saveBlockstoBlockchainDB
from config import TEMP_BLOCK_PATH
from consensus.consensus_main import consensus_trigger
from lib.config_system import get_config
from lib.log import get_logger
from lib.perpetualtimer import perpetualTimer
from node.unl import Unl
from transactions.pending_to_validating import PendinttoValidating
from transactions.save_to_my_transaction import SavetoMyTransaction
from wallet.wallet import PrivateKey
from wallet.wallet import PublicKey
from wallet.wallet import Signature
from wallet.wallet import Wallet_Import

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
        previous_hash="fb8b69c2276c8316c64a5d34b5f3063d1f8b8dc17cda7ee84fa1343978d464a9",
    ):
        self.genesis_time = int(time.time())
        self.start_time = int(time.time())
        self.block_time = 7
        self.block_time_change_time = int(time.time())
        self.block_time_change_block = 0

        self.newly = False

        self.previous_hash = previous_hash
        self.sequance_number = 0
        self.empty_block_number = 0

        blocks_hash = [self.previous_hash]
        SaveBlockshash(blocks_hash)

        accounts_list = GetAccounts()
        if accounts_list == []:
            save_accounts([Account(creator, 1000000000)])

        self.edited_accounts = []

        self.pendingTransaction = []
        self.validating_list = []
        self.transaction_fee = 0.02
        self.default_transaction_fee = 0.02
        # Each user settings by our hardware
        self.default_optimum_transaction_number = 10
        self.default_increase_of_fee = 0.01

        self.hash = None

        self.max_tx_number = 2
        self.minumum_transfer_amount = 1000

        self.raund_1_starting_time = None
        self.raund_1_time = 2.3333333333333335
        self.raund_1 = False
        self.raund_1_node = False

        self.raund_2_starting_time = None
        self.raund_2_time = 2.3333333333333335
        self.raund_2 = False
        self.raund_2_node = False

        self.consensus_timer = 0.50

        self.increase_the_time = 0
        self.increase_the_time_2 = 0
        self.decrease_the_time = 0
        self.decrease_the_time_2 = 0

        self.validated = False
        self.validated_time = None

        self.dowload_true_block = ""

        self.save_block()

        logger.info("Consensus timer is started")
        perpetualTimer(self.consensus_timer, consensus_trigger).start()

    def reset_the_block(self):
        """
        When the block is verified and if block have a transaction
        and if block have at least half of the max_tx_number transaction,it saves the block
        and makes the edits for the new block.
        """

        if self.increase_the_time == 3:
            self.increase_the_time = 0
            self.raund_1_time += 0.1
            self.block_time_change_time = int(time.time())
            self.block_time_change_block = self.sequance_number

        if self.decrease_the_time == 3:
            self.decrease_the_time = 0
            if not self.raund_1_time <= 2:
                self.raund_1_time -= 0.1
                self.block_time_change_time = int(time.time())
                self.block_time_change_block = self.sequance_number

        if self.increase_the_time_2 == 3:
            self.increase_the_time_2 = 0
            self.raund_2_time += 0.1
            self.block_time_change_time = int(time.time())
            self.block_time_change_block = self.sequance_number

        if self.decrease_the_time_2 == 3:
            self.decrease_the_time_2 = 0
            if not self.raund_2_time <= 2:
                self.raund_2_time -= 0.1
                self.block_time_change_time = int(time.time())
                self.block_time_change_block = self.sequance_number

        self.block_time = self.raund_1_time + self.raund_2_time

        self.start_time = int(time.time())

        self.raund_1_starting_time = None
        self.raund_1 = False
        self.raund_1_node = False

        self.raund_2_starting_time = None
        self.raund_2 = False
        self.raund_2_node = False

        self.validated = False

        # Resetting the node candidate blocks.
        for node in Unl.get_as_node_type(Unl.get_unl_nodes()):
            node.candidate_block = None
            node.candidate_block_hash = None

        if not len(self.validating_list) == 0 and not len(
                self.validating_list) < (self.max_tx_number / 2):

            app_tigger(self)

            my_address = Wallet_Import(-1, 3)
            for tx in self.validating_list:
                if tx.toUser == my_address:
                    SavetoMyTransaction(tx)

            saveBlockstoBlockchainDB(self)

            # Resetting and setting the new elements.
            self.previous_hash = self.hash
            current_blockshash_list = GetBlockshash()
            current_blockshash_list.append(self.previous_hash)
            SaveBlockshash(current_blockshash_list)
            self.sequance_number = self.sequance_number + 1
            self.validating_list = []
            self.hash = None

            logger.info("New block created")
        else:
            logger.info(
                "New block not created because any transaction is not validated"
            )
            self.empty_block_number += 1

        logger.debug(self.__dict__)

        # Adding self.pendingTransaction to the new/current block.
        PendinttoValidating(self)

        # Saving the new block.
        self.save_block()

    def save_block(self):
        """
        Saves the current block to the TEMP_BLOCK_PATH.
        """

        os.chdir(get_config()["main_folder"])
        with open(TEMP_BLOCK_PATH, "wb") as block_file:
            pickle.dump(self, block_file, protocol=2)
