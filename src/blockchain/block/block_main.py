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

from node.myownp2pn import mynode
from node.unl import get_unl_nodes, get_as_node_type

from transactions.transaction import Transaction
from transactions.pending_to_validating import PendinttoValidating
from transactions.save_to_my_transaction import SavetoMyTransaction

from accounts.account import Account, save_accounts, save_accounts_part
from accounts.get_balance import GetBalance
from accounts.get_sequance_number import GetSequanceNumber

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
    def __init__(self, sequance_number, creator):
        # TODO: What to do in case of consensus fails will be added

        self.genesis_time = int(time.time())
        self.start_time = int(time.time())
        self.block_time = 7
        self.block_time_change_time = int(time.time())
        self.block_time_change_block = sequance_number

        self.newly = False 

        self.previous_hash = "0"
        self.sequance_number = sequance_number
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

    def propagating_the_tx(self, tx):
        """
        Sends the given transaction to UNL nodes.
        """
        items = {
            "transactionrequest": 1,
            "sequance_number": tx.sequance_number,
            "signature": tx.signature,
            "fromUser": tx.fromUser,
            "to_user": tx.toUser,
            "data": tx.data,
            "amount": tx.amount,
            "transaction_fee": tx.transaction_fee,
            "transaction_time":tx.time
        }
        for each_node in get_as_node_type(get_unl_nodes()):
            mynode.main_node.send_data_to_node(each_node, items)

    def createTrans(self, sequance_number, signature, fromUser, toUser, transaction_fee, data, amount, transaction_time, transaction_sender=None):

      # Printing the info of tx
      dprint("\nCreating the transaction")
      dprint("***")
      dprint(sequance_number)
      dprint(signature)
      dprint(fromUser)
      dprint(toUser)
      dprint(data)
      dprint(amount)
      dprint("***\n")
      # End

      # Some data
      signature_class = Signature.fromBase64(signature)
      temp_signature = signature_class.toBase64()

      already_got = self.tx_already_got(fromUser, sequance_number, temp_signature)
      # End

      # Validation
      dprint("\nValidation")
      if Ecdsa.verify((str(sequance_number)+str(fromUser)+str(toUser)+str(data)+str(amount)+str(transaction_fee)+str(transaction_time)), signature_class, PublicKey.fromPem(fromUser)) and not amount < self.minumum_transfer_amount and not transaction_fee < self.transaction_fee and not already_got and not (int(time.time()) - transaction_time) > 60:
        dprint("Signature is valid")

        dprint("Getsequancenumber: "+str(GetSequanceNumber(fromUser, self)+1))
        if sequance_number == (GetSequanceNumber(fromUser, self)+1):
          dprint("Sequance number is valid")

          balance = GetBalance(fromUser, self)

          if balance >= (float(amount)+float(transaction_fee)) and (balance - (float(amount)+float(transaction_fee))) > 2:
            dprint("Amount is valid")

            # Local saving
            the_tx = Transaction(
                sequance_number= sequance_number,
                signature=temp_signature,
                fromUser= fromUser,
                toUser=toUser,
                data = data,
                amount = amount,
                transaction_fee= transaction_fee,
                time_of_transaction = transaction_time
            )
            self.pendingTransaction.append(the_tx)
            self.change_transaction_fee()
            self.save_block()
            # End

            self.propagating_the_tx(the_tx)

            return the_tx

      dprint(" Validation end")
      # End

    def tx_already_got(self, fromUser, sequance_number, temp_signature):
        for already_tx in (self.pendingTransaction + self.validating_list):
            if already_tx.signature == temp_signature:
                return True
            if already_tx.fromUser == fromUser:
                for already_tx_parent in (self.pendingTransaction + self.validating_list):
                    if not temp_signature == already_tx_parent.signature:
                        if sequance_number == already_tx_parent.sequance_number:
                            return True

        return False

    def send_my_response_on_transaction(self, temp_transaction, response, transaction_sender):
        items = {
            "transactionresponse": 1,
            "fromUser": mynode.main_node.id,
            "response": response,
            "transaction_signature": temp_transaction.signature,
            "signature": Ecdsa.sign(
                response+str(temp_transaction.signature),
                PrivateKey.fromPem(Wallet_Import(0, 1))
                ).toBase64()
        }
        mynode.main_node.send_data_to_node(transaction_sender, items)

    def save_block(self):
        os.chdir(get_config()["main_folder"])
        with open(TEMP_BLOCK_PATH, 'wb') as block_file:
            pickle.dump(self, block_file, protocol=2)

    def change_transaction_fee(self):
        """
        Increase transaction fee by 0.01 DNC for each self.default_optimum_transaction_number argument
        """
        if not (len(self.pendingTransaction + self.validating_list) // self.default_optimum_transaction_number) == 0:
            increase = (len(self.pendingTransaction + self.validating_list) // self.default_optimum_transaction_number) * self.default_increase_of_fee
            self.transaction_fee += increase
        else:
            self.transaction_fee = self.default_transaction_fee
