#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import hashlib

import pprint

from wallet.wallet import Ecdsa, PrivateKey, PublicKey, Wallet_Import, Signature

import pickle


from lib.settings_system import the_settings
from lib.mixlib import dprint

import os


import time


from config import *

class Account:
    def __init__(self, PublicKey, balance):
        self.PublicKey = PublicKey
        self.sequance_number = 0
        self.balance = balance


class ledger:
    def __init__(self, creator):
        self.Accounts = [Account(creator, balance=1000000)]
        self.pendingTransaction = []
        self.validating_list = []
        self.save_ledger()

    def Verificate_Pending_Trans(self):
        dprint("Pending transactions number: "+str(len(self.pendingTransaction)))
        dprint("Validating transactions number: "+str(len(self.validating_list)))
        if len(self.pendingTransaction) > 2 and not len(self.validating_list) > 2:
            for tx in self.pendingTransaction:
                self.validating_list.append(tx)
            self.pendingTransaction.clear()

        for trans in self.validating_list:
            if self.tx_verification(trans):
                touser_inlist = False
                for Accounts in self.Accounts:
                    if Accounts.PublicKey in trans.fromUser:
                        Accounts.balance -= (float(trans.amount)+trans.transaction_fee)
                        Accounts.sequance_number += 1
                    elif Accounts.PublicKey in trans.toUser:
                        Accounts.balance += float(trans.amount)
                        touser_inlist = True
                if not touser_inlist:
                    self.Accounts.append(Account(trans.toUser, float(trans.amount)))
                self.validating_list.remove(trans)

                for folder_entry in os.scandir('apps'):
                    if ".md" not in folder_entry.name:
                        for entry in os.scandir("apps/"+folder_entry.name):
                            if entry.is_file():
                                if entry.name[0] != '_' and ".py" in entry.name and "_main" in entry.name:
                                    import_command = f"from apps.{folder_entry.name}.{entry.name.replace('.py','')} import {entry.name.replace('.py','')}_tx"
                                    tx_command = f"{entry.name.replace('.py','')}_tx(trans)"
                                    exec (import_command)
                                    exec (tx_command)

        dprint("End mining pending transactions number: "+str(len(self.pendingTransaction)))
        dprint("End mining validating transactions number: "+str(len(self.validating_list)))

        self.save_ledger()

    def tx_verification(self, tx):
        if len(tx.valid) >= (len(tx.total_validators) / 3):
            return True
        elif len(tx.invalid) >= (len(tx.total_validators) / 3):
            self.validating_list.remove(trans)
        else:
            if (len(tx.valid) + len(tx.invalid)) != len(tx.total_validators):
             from node.myownp2pn import MyOwnPeer2PeerNode
             exclude_list = []
             for already_asked in tx.already_asked_nodes:
                 already_responsed = False
                 for sended_response_node in (tx.valid + tx.invalid):
                     if already_asked[1] == sended_response_node[1]:
                         already_responsed = True

                 if not already_responsed:
                     if (int(time.time()) - already_asked[0]) <= 60:
                         exclude_list.append(already_asked[1])
                 else:
                     exclude_list.append(already_asked[1])

             dprint("exclude list_in ledger"+str(exclude_list))
             from node.unl import get_as_node_type
             nodes_list = get_as_node_type(tx.total_validators)
             dprint("Nodes list: "+str(nodes_list))
             for node in nodes_list:
                 if node not in get_as_node_type(exclude_list):
                    temp_already_asked = []
                    temp_already_asked.append(int(time.time()))
                    temp_already_asked.append(node.id)
                    tx.already_asked_nodes.append(temp_already_asked)
                    MyOwnPeer2PeerNode.main_node.send_to_node(node, {"transactionrequest": 1, "sequance_number": tx.sequance_number, "signature": tx.signature, "fromUser": tx.fromUser, "to_user": tx.toUser, "data": tx.data, "amount": tx.amount, "transaction_fee": tx.transaction_fee, "response": True})

    def createTrans(self, sequance_number, signature, fromUser, toUser, transaction_fee, data = None, amount = None, transaction_sender = None, response = False):

      dprint("\nCreating transaction.")
      signature_class = Signature.fromBase64(signature)
      dprint("***")
      dprint(sequance_number)
      dprint(signature)
      dprint(fromUser)
      dprint(toUser)
      dprint(data)
      dprint(amount)
      dprint("***\n")
      dprint(Ecdsa.verify((str(sequance_number)+str(fromUser)+str(toUser)+str(data)+str(amount)+str(transaction_fee)), signature_class, PublicKey.fromPem(fromUser)))
      
      temp_signature = signature_class.toBase64()
      already_in_pending = False
      for already_tx in (self.pendingTransaction + self.validating_list):
          if already_tx.signature == temp_signature:
              already_in_pending = True
      if Ecdsa.verify((str(sequance_number)+str(fromUser)+str(toUser)+str(data)+str(amount)+str(transaction_fee)), signature_class, PublicKey.fromPem(fromUser)):
        if sequance_number == (self.getSequanceNumber(fromUser)+1) or already_in_pending:
          dprint("Sign verify is true.")
          if (self.getBalance(fromUser) >= (float(amount)+float(transaction_fee)) and float(amount) != float(0)) or response == False:
               temp_transaction = Transaction(sequance_number= sequance_number, signature=signature_class.toBase64(), fromUser= fromUser, toUser=toUser, data = data, amount = amount, transaction_fee= transaction_fee)
               dprint("Balance controll is true.")
               if already_in_pending == False:
                   self.pendingTransaction.append(temp_transaction)
                   self.save_ledger()
               from node.myownp2pn import MyOwnPeer2PeerNode
               dprint("imported myownpeer2peernode")
               if transaction_sender is None:
                   if already_in_pending == False:
                       MyOwnPeer2PeerNode.main_node.send_to_nodes({"transactionrequest": 1, "sequance_number": sequance_number, "signature": signature, "fromUser": fromUser, "to_user": toUser, "data": data, "amount": amount, "transaction_fee": transaction_fee, "response": False})
               else:
                   dprint(str(response))
                   if response:
                       self.send_my_response_on_transaction(temp_transaction= temp_transaction, response= "TRUE", transaction_sender= transaction_sender)
                   if already_in_pending == False:
                       MyOwnPeer2PeerNode.main_node.send_to_nodes({"transactionrequest": 1, "sequance_number": sequance_number, "signature": signature, "fromUser": fromUser, "to_user": toUser, "data": data, "amount": amount, "transaction_fee": transaction_fee, "response": False}, exclude=[transaction_sender])
               self.Verificate_Pending_Trans()
               return True
          else:
              if transaction_sender != None and response == True:
                  self.send_my_response_on_transaction(temp_transaction= temp_transaction, response= "FALSE", transaction_sender= transaction_sender)
      else:
         if transaction_sender != None and response == True:
             self.send_my_response_on_transaction(temp_transaction= temp_transaction, response= "FALSE", transaction_sender= transaction_sender)

    def send_my_response_on_transaction(self, temp_transaction, response, transaction_sender):
        from node.myownp2pn import MyOwnPeer2PeerNode
        MyOwnPeer2PeerNode.main_node.send_to_node(transaction_sender, {"transactionresponse": 1, "fromUser": MyOwnPeer2PeerNode.main_node.id, "response": response, "transaction_signature": temp_transaction.signature, "signature": Ecdsa.sign(response+str(temp_transaction.signature), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()})

    def getBalance(self, user):
        balance = 0
        user = user.replace('\n', '')
        for Accounts in self.Accounts:
            temp_pubkey = Accounts.PublicKey.replace('\n', '')
            if temp_pubkey in user or temp_pubkey == user:
                balance = Accounts.balance
                for trans in self.pendingTransaction + self.validating_list:
                    for Accounts in self.Accounts:
                        if temp_pubkey in trans.fromUser.replace('\n', '') or temp_pubkey == trans.fromUser.replace('\n', ''):
                            balance -= (float(trans.amount)-trans.transaction_fee)
                        elif temp_pubkey in trans.toUser.replace('\n', '') or temp_pubkey == trans.toUser.replace('\n', ''):
                            balance += float(trans.amount)
                return balance
        return balance
        
    def getSequanceNumber(self, user):
        sequance_number = 0
        user = user.replace('\n', '')
        for Accounts in self.Accounts:

            temp_pubkey = Accounts.PublicKey.replace('\n', '')

            if temp_pubkey in user or temp_pubkey == user:
  
                sequance_number = Accounts.sequance_number

                for trans in self.pendingTransaction + self.validating_list:

                    if user in trans.fromUser.replace('\n', '') or user == trans.fromUser.replace('\n', ''):
                        sequance_number += 1
                return sequance_number
        return sequance_number

    def save_ledger(self):
        from lib.config_system import get_config
        import os


        os.chdir(get_config()["main_folder"])
        with open(LEDGER_PATH, 'wb') as ledger_file:
            pickle.dump(self, ledger_file, protocol=2)



class Transaction:
    def __init__(self, sequance_number, signature, fromUser, toUser, data, amount, transaction_fee):
        self.sequance_number = sequance_number
        self.signature = signature
        self.fromUser = fromUser
        self.toUser = toUser
        self.data = data
        self.amount = amount
        self.transaction_fee = transaction_fee
        self.valid = []
        from node.unl import get_unl_nodes
        self.total_validators = get_unl_nodes()
        self.already_asked_nodes = []
        self.invalid = []


def get_ledger():
        from lib.config_system import get_config
        import os


        os.chdir(get_config()["main_folder"])
        with open(LEDGER_PATH, 'rb') as ledger_file:
            return pickle.load(ledger_file)



def sendme_full_node_list():
    from node.myownp2pn import MyOwnPeer2PeerNode
    from node.unl import get_unl_nodes, get_as_node_type
    node = MyOwnPeer2PeerNode.main_node
    unl_list = get_as_node_type(get_unl_nodes())
    node.send_to_node(unl_list[0], "sendmefullnodelist")


def get_ledger_from_other_node():
    from node.myownp2pn import MyOwnPeer2PeerNode
    from node.unl import get_unl_nodes, get_as_node_type
    node = MyOwnPeer2PeerNode.main_node
    unl_list = get_as_node_type(get_unl_nodes())
    node.send_to_node(unl_list[0], "sendmefullledger")


def create_ledger():

    if the_settings()["test_mode"]:
        dprint("Creating new ledger")
        system = ledger(Wallet_Import(0,0))
        from node.myownp2pn import MyOwnPeer2PeerNode
        MyOwnPeer2PeerNode.main_node.send_full_chain()
    else:
        dprint("Getting ledger from nodes")
        get_ledger()
