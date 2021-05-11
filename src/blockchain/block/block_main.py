#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import pickle
import sqlite3
import time
import os

from lib.settings_system import the_settings
from lib.mixlib import dprint
from lib.config_system import get_config
from lib.merkle_root import MerkleTree
from lib.perpetualtimer import perpetualTimer

from node.myownp2pn import mynode
from node.unl import get_unl_nodes, get_as_node_type

from wallet.wallet import Ecdsa, PrivateKey, PublicKey, Wallet_Import, Signature

from accounts.account import Account

from transactions.transaction import Transaction

from blockchain.block.candidate_blocks import get_candidate_block

from consensus.consensus_main import consensus_trigger

from app.app_main import apps_starter, app_tigger

from config import *


class Block:
    def __init__(self, sequance_number, creator):

        # TODO: What to do in case of consensus fails will be added

        self.start_time = int(time.time())
        self.block_time = 7

        self.previous_hash = "0"
        self.sequance_number = sequance_number
        self.Accounts = [Account(creator, balance=1000000)]
        self.pendingTransaction = []


        self.validating_list = []
        self.validating_list_time = 2
        self.validating_list_starting_time = int(time.time())

        self.hash = None

        from node.unl import get_unl_nodes
        self.total_validators = get_unl_nodes()

        self.max_tx_number = 2

        self.raund_1_starting_time = None
        self.raund_1_time = 3
        self.raund_1 = False
        self.raund_1_node = False
        
        self.raund_2_starting_time = None
        self.raund_2_time = 3
        self.raund_2 = False
        self.raund_2_node = False

        self.consensus_timer = 0.50

        self.validated = False

        self.dowload_true_block = ""

        self.save_block()
        perpetualTimer(self.consensus_timer,consensus_trigger).start()
        apps_starter()


    def calculate_hash(self):

        tx_list = []
        dprint(len(self.validating_list))
        for element in self.validating_list[:]:
            dprint(element)
            tx_list.append(element.signature)

        dprint(tx_list)

        if len(tx_list) != 0:
            tx_hash = MerkleTree(tx_list).getRootHash()
        else:
            tx_hash = "0"

        ac_list = []
        for element in self.Accounts[:]:
            ac_list.append(element.PublicKey)

        dprint(ac_list)

        ac_hash = MerkleTree(ac_list).getRootHash()
        

        main_list = []

        main_list.append(self.previous_hash)

        main_list.append(str(self.sequance_number))

        main_list.append(ac_hash)

        main_list.append(tx_hash)

        dprint(main_list)


        self.hash = MerkleTree(main_list).getRootHash()

        dprint(self.hash)


    def proccess_the_transaction(self):

        from_user_list = []
    
        for trans in self.validating_list:
                touser_inlist = False
                for Accounts in self.Accounts:
                    if Accounts.PublicKey == trans.fromUser:
                        Accounts.balance -= (float(trans.amount)+trans.transaction_fee)
                        Accounts.sequance_number += 1
                        from_user_list.append(Accounts)
                    elif Accounts.PublicKey == trans.toUser:
                        Accounts.balance += float(trans.amount)
                        touser_inlist = True
                if not touser_inlist:
                    self.Accounts.append(Account(trans.toUser, float(trans.amount)))
                    
        temp_validating_list = self.validating_list

        for tx_item in temp_validating_list[:]:
            for Account_item in from_user_list:
                if tx_item.fromUser == Account_item.PublicKey:
                    tx_item.fromUser = Account_item

        temp_validating_list = sorted(temp_validating_list, key=lambda x: self.Accounts.index(x.fromUser))




        for temp_validating_list_item in temp_validating_list[:]:
            temp_validating_list_item.fromUser = temp_validating_list_item.fromUser.PublicKey


        self.validating_list = temp_validating_list





    def reset_the_block(self):
        
        dprint("""\n
  _____                          _     ____  _      ____   _____ _  __
 / ____|                        | |   |  _ \| |    / __ \ / ____| |/ /
| |    _   _ _ __ _ __ ___ _ __ | |_  | |_) | |   | |  | | |    | ' / 
| |   | | | | '__| '__/ _ \ '_ \| __| |  _ <| |   | |  | | |    |  <  
| |___| |_| | |  | | |  __/ | | | |_  | |_) | |___| |__| | |____| . \ 
 \_____\__,_|_|  |_|  \___|_| |_|\__| |____/|______\____/ \_____|_|\_\
                                        
        """+str(self.__dict__)+"\n")

        app_tigger(self)


        db = sqlite3.connect(BLOCKCHAIN_PATH)
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS blockchain(
                    previous_hash,
                    sequance_number,
                    hash
                );""")

        cur.execute(f"""INSERT INTO blockchain VALUES (
            '{self.previous_hash}', '{self.sequance_number}', '{self.hash}'
        )""")


        cur.execute(f"""CREATE TABLE accounts{self.sequance_number}(
                    PublicKey,
                    sequance_number,
                    balance
                );""")
        for each_account in self.Accounts:
            cur.execute(f"""INSERT INTO accounts{self.sequance_number} VALUES (?,?,?)""",
                [each_account.PublicKey, each_account.sequance_number, each_account.balance]
            )
        cur.execute(f"""CREATE TABLE transactions{self.sequance_number}(
                    sequance_number,
                    signature,
                    fromUser,
                    toUser,
                    data,
                    amount,
                    transaction_fee
                );""")
        for each_transaction in self.validating_list:
            cur.execute(f"""INSERT INTO transactions{self.sequance_number} VALUES (?,?,?,?,?,?,?)""",
                [each_transaction.sequance_number, each_transaction.signature, each_transaction.fromUser, each_transaction.toUser, each_transaction.data, each_transaction.amount, each_transaction.transaction_fee]
            )


        db.commit()
        db.close()

        self.previous_hash = self.hash
        self.sequance_number = self.sequance_number + 1
        self.validating_list = []
        self.validating_list_starting_time = int(time.time())
        
        self.hash = None

        candidate_class = get_candidate_block()
        candidate_class.candidate_blocks = []
        candidate_class.candidate_block_hashes = []
        candidate_class.save_candidate_blocks()





        self.raund_1_starting_time = None
        self.raund_1 = False
        self.raund_1_node = False
        
        self.raund_2_starting_time = None
        self.raund_2 = False
        self.raund_2_node = False


        self.validated = False



        dprint("""\n
 _   _                 ____  _      ____   _____ _  __
| \ | |               |  _ \| |    / __ \ / ____| |/ /
|  \| | _____      __ | |_) | |   | |  | | |    | ' / 
| . ` |/ _ \ \ /\ / / |  _ <| |   | |  | | |    |  <  
| |\  |  __/\ V  V /  | |_) | |___| |__| | |____| . \ 
|_| \_|\___| \_/\_/   |____/|______\____/ \_____|_|\_\
                                        
        """+str(self.__dict__)+"\n")

        self.Verificate_Pending_Trans()
        self.save_block()


    def Verificate_Pending_Trans(self):
        dprint("Pending transactions number: "+str(len(self.pendingTransaction)))
        dprint("Validating transactions number: "+str(len(self.validating_list)))
        print(self.raund_1_starting_time)
        if len(self.validating_list) < self.max_tx_number and self.raund_1_starting_time is None:
            for tx in self.pendingTransaction[:]:
                if len(self.validating_list) < self.max_tx_number:
                    self.validating_list.append(tx)
                    self.pendingTransaction.remove(tx)

       
      


        dprint("End mining pending transactions number: "+str(len(self.pendingTransaction)))
        dprint("End mining validating transactions number: "+str(len(self.validating_list)))



    def propagating_the_tx(self,tx):
        # Propagating to other nodes
        from node.myownp2pn import mynode
        from node.unl import get_as_node_type
        for each_node in get_as_node_type(self.total_validators):
            mynode.main_node.send_data_to_node(each_node,{"transactionrequest": 1, "sequance_number": tx.sequance_number, "signature": tx.signature, "fromUser": tx.fromUser, "to_user": tx.toUser, "data": tx.data, "amount": tx.amount, "transaction_fee": tx.transaction_fee})
        # End  



    def createTrans(self, sequance_number, signature, fromUser, toUser, transaction_fee, data, amount, transaction_sender = None):

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
      
      already_got = self.tx_already_got(temp_signature)
      # End


      # Validation
      dprint("\nValidation")
      if Ecdsa.verify((str(sequance_number)+str(fromUser)+str(toUser)+str(data)+str(amount)+str(transaction_fee)), signature_class, PublicKey.fromPem(fromUser)) and already_got == False:
        dprint("Signature is valid")

        dprint("Getsequancenumber: "+str(self.getSequanceNumber(fromUser)+1))
        if sequance_number == (self.getSequanceNumber(fromUser)+1):
          dprint("Sequance number is valid")

          balance = self.getBalance(fromUser)

          if balance >= (float(amount)+float(transaction_fee)) and (balance - (float(amount)+float(transaction_fee))) > 2:
            dprint("Amount is valid")



            

            # Local saving
            the_tx = Transaction(sequance_number= sequance_number, signature=temp_signature, fromUser= fromUser, toUser=toUser, data = data, amount = amount, transaction_fee= transaction_fee)
            self.pendingTransaction.append(the_tx)
            self.Verificate_Pending_Trans()
            self.save_block()
            # End
            
            self.propagating_the_tx(the_tx)
            

            return True
            
      dprint(" Validation end")
      # End



    def tx_already_got(self,temp_signature):
      for already_tx in (self.pendingTransaction + self.validating_list):
          if already_tx.signature == temp_signature:
              return True
      return False

    def send_my_response_on_transaction(self, temp_transaction, response, transaction_sender):
        from node.myownp2pn import mynode
        mynode.main_node.send_data_to_node(transaction_sender, {"transactionresponse": 1, "fromUser": mynode.main_node.id, "response": response, "transaction_signature": temp_transaction.signature, "signature": Ecdsa.sign(response+str(temp_transaction.signature), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()})

    def getBalance(self, user):
        balance = 0
        user = "".join([
            l.strip() for l in user.splitlines()
            if l and not l.startswith("-----")
        ])
        for Accounts in self.Accounts:

            if Accounts.PublicKey == user:
                balance = Accounts.balance
                return balance
        return balance
        
    def getSequanceNumber(self, user):
        sequance_number = 0
        for Accounts in self.Accounts:


            if Accounts.PublicKey == user:
  
                sequance_number = Accounts.sequance_number


                for trans in self.pendingTransaction + self.validating_list:
                    if user == trans.fromUser:
                        sequance_number += 1

                return sequance_number
        return sequance_number

    def save_block(self):

        os.chdir(get_config()["main_folder"])
        with open(TEMP_BLOCK_PATH, 'wb') as block_file:
            pickle.dump(self, block_file, protocol=2)









def get_block():

    os.chdir(get_config()["main_folder"])
    with open(TEMP_BLOCK_PATH, 'rb') as block_file:
        return pickle.load(block_file)



def sendme_full_node_list():

    node = mynode.main_node
    unl_list = get_as_node_type(get_unl_nodes())
    node.send_data_to_node(unl_list[0], "sendmefullnodelist")


def get_block_from_other_node():

    node = mynode.main_node
    unl_list = get_as_node_type(get_unl_nodes())
    node.send_data_to_node(unl_list[0], "sendmefullblock")


def create_block():

    if the_settings()["test_mode"]:
        dprint("Creating new block")
        pubkey = "".join([
            l.strip() for l in Wallet_Import(0,0).splitlines()
            if l and not l.startswith("-----")
        ])        
        Block(0,pubkey)
        mynode.main_node.send_full_chain()
    else:
        dprint("Getting block from nodes")
        get_block()
