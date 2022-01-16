#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import pickle
import time
import os

from lib.mixlib import dprint
from lib.config_system import get_config
from lib.perpetualtimer import perpetualTimer

from node.unl import get_unl_nodes, get_as_node_type

from transactions.pending_to_validating import PendinttoValidating
from transactions.save_to_my_transaction import SavetoMyTransaction

from accounts.account import Account
from accounts.save_accounts import save_accounts
from accounts.save_accounts_part import save_accounts_part

from blockchain.block.save_block_to_blockchain_db import saveBlockstoBlockchainDB
from blockchain.block.blocks_hash import SaveBlockshash, GetBlockshash, SaveBlockshash_part

from wallet.wallet import (
    Ecdsa,
    PrivateKey,
    PublicKey,
    Wallet_Import,
    Signature
    )

from consensus.consensus_main import consensus_trigger

from app.app_main import apps_starter, app_tigger

from config import TEMP_BLOCK_PATH


class Block:
    """
    Block class is most important class. It is responsible for 
    resetting and saving blocks.

    You must give a creator of the block. This creator will 
    own all the coins.
    """

    def __init__(self, creator):
        self.genesis_time = int(time.time())
        self.start_time = int(time.time())
        self.block_time = 7
        self.block_time_change_time = int(time.time())
        self.block_time_change_block = 0

        self.newly = False 

        self.previous_hash = "0"
        self.sequance_number = 0
        self.empty_block_number = 0

        blocks_hash = [self.previous_hash]
        SaveBlockshash(blocks_hash)
        SaveBlockshash_part([])

        accounts = [
            Account(creator, balance=1000000000)
            ]
        save_accounts(accounts)
        save_accounts_part([])
        self.edited_accounts = []

        self.pendingTransaction = []
        self.validating_list = []
        self.transaction_fee = 0.02
        self.default_transaction_fee = 0.02
        self.default_optimum_transaction_number = 10 # Each user settings by our hardware
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
        perpetualTimer(self.consensus_timer, consensus_trigger).start()
        apps_starter()

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


        #Printing validated block.
        dprint("""\n
  _____                          _     ____  _      ____   _____ _  __
 / ____|                        | |   |  _ \| |    / __ \ / ____| |/ /
| |    _   _ _ __ _ __ ___ _ __ | |_  | |_) | |   | |  | | |    | ' / 
| |   | | | | '__| '__/ _ \ '_ \| __| |  _ <| |   | |  | | |    |  <  
| |___| |_| | |  | | |  __/ | | | |_  | |_) | |___| |__| | |____| . \ 
 \_____\__,_|_|  |_|  \___|_| |_|\__| |____/|______\____/ \_____|_|\_\
                                        
        """+str(self.__dict__)+"\n")

        self.start_time = int(time.time())

        self.raund_1_starting_time = None
        self.raund_1 = False
        self.raund_1_node = False

        self.raund_2_starting_time = None
        self.raund_2 = False
        self.raund_2_node = False

        self.validated = False

        

        # Resetting the node candidate blocks.
        for node in get_as_node_type(get_unl_nodes()):
            node.candidate_block = None
            node.candidate_block_hash = None

        if not len(self.validating_list) == 0 and not len(self.validating_list) < (self.max_tx_number / 2):

            
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

            #Printing new block.
            dprint("""\n
    _   _                 ____  _      ____   _____ _  __
    | \ | |               |  _ \| |    / __ \ / ____| |/ /
    |  \| | _____      __ | |_) | |   | |  | | |    | ' / 
    | . ` |/ _ \ \ /\ / / |  _ <| |   | |  | | |    |  <  
    | |\  |  __/\ V  V /  | |_) | |___| |__| | |____| . \ 
    |_| \_|\___| \_/\_/   |____/|______\____/ \_____|_|\_\
                                            
            """+str(self.__dict__)+"\n")
        else:
            self.empty_block_number += 1



        # Adding self.pendingTransaction to the new/current block.
        PendinttoValidating(self)

        # Saving the new block.
        self.save_block()

    def save_block(self):
        """
        Saves the current block to the TEMP_BLOCK_PATH.
        """

        os.chdir(get_config()["main_folder"])
        with open(TEMP_BLOCK_PATH, 'wb') as block_file:
            pickle.dump(self, block_file, protocol=2)
