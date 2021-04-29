#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import hashlib

import pprint

from wallet.wallet import Ecdsa, PrivateKey, PublicKey, Wallet_Import, Signature

import pickle
import json


from lib.settings_system import the_settings
from lib.mixlib import dprint

import os


import time


from config import *


from blockchain.block.account import Account
from blockchain.block.transaction import Transaction


import time

from threading import Timer,Thread,Event

from func.merkle_root import MerkleTree

def consensus_trigger():
      print("consensus trigger")
      get_block().consensus()


class app(Thread):
    def __init__(self,import_command,func):
        Thread.__init__(self)
        self.import_command = import_command
        self.func = func 
        print("\n\n in app class")

    def run(self):
        print("\n\n in app runner")
        exec(self.import_command)
        exec(self.func)

class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

      for folder_entry in os.scandir('apps'):
            if ".md" not in folder_entry.name:
                for entry in os.scandir("apps/"+folder_entry.name):
                    if entry.is_file():
                        if entry.name[0] != '_' and ".py" in entry.name and "_main" in entry.name:
                            import_command = f"from apps.{folder_entry.name}.{entry.name.replace('.py','')} import {entry.name.replace('.py','')}_run"
                            tx_command = f"{entry.name.replace('.py','')}_run()"

                            exec (import_command)

                            print("\n\ntest")
                            print(import_command)
                            print(tx_command)
                            x = app(import_command,tx_command)
                            x.start()


   def handle_function(self):
      
      if not get_block().validated:
       self.hFunction()
       self.thread = Timer(self.t,self.handle_function)
       self.thread.start()
      else:
          self.cancel()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()






class Block:
    def __init__(self, sequance_number, creator):


        # TODO: Save the block to blockchain before resetting
        # TODO: What to do in case of consensus fails will be added


        self.previous_hash = "0"
        self.sequance_number = sequance_number
        self.Accounts = [Account(creator, balance=1000000)]
        self.pendingTransaction = []


        self.validating_list = []
        self.validating_list_time = 3
        self.validating_list_starting_time = int(time.time())

        self.hash = None

        from node.unl import get_unl_nodes
        self.total_validators = get_unl_nodes()
        self.candidate_blocks = []
        self.candidate_block_hashes = []


        self.max_tx_number = 2


        self.raund_1_starting_time = None
        self.raund_1_time = 6
        self.raund_1 = False
        self.raund_1_node = False
        
        self.raund_2_starting_time = None
        self.raund_2_time = 6
        self.raund_2 = False
        self.raund_2_node = False


        self.consensus_timer = 1


        self.validated = False

        self.dowload_true_block = ""

        self.save_block()
        perpetualTimer(self.consensus_timer,consensus_trigger).start()

    def calculate_hash(self):


        tx_item_list = []


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

        from hashlib import sha256
        

        main_list = []

        main_list.append(self.previous_hash)

        main_list.append(str(self.sequance_number))

        main_list.append(ac_hash)

        main_list.append(tx_hash)

        dprint(main_list)


        self.hash = MerkleTree(main_list).getRootHash()

        dprint(self.hash)
    
    def proccess_the_transaction(self):

        for start_validating_list_item in self.validating_list:
            print(start_validating_list_item.fromUser)

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

         
        for end_validating_list_item in self.validating_list:
            print(start_validating_list_item.fromUser)


    def consensus(self):
      if not (int(time.time()) - self.validating_list_starting_time) < self.validating_list_time:
        #or len(self.validating_list) == self.max_tx_number
        if self.raund_1_starting_time == None:
            self.raund_1_starting_time = int(time.time())
        if not self.raund_1:

            self.consensus_raund_1()
        elif not self.raund_2:
            self.consensus_raund_2()



    def app_tigger(self):
            for trans in self.validating_list:
                for folder_entry in os.scandir('apps'):
                    if ".md" not in folder_entry.name:
                        for entry in os.scandir("apps/"+folder_entry.name):
                            if entry.is_file():
                                if entry.name[0] != '_' and ".py" in entry.name and "_main" in entry.name:
                                    import_command = f"from apps.{folder_entry.name}.{entry.name.replace('.py','')} import {entry.name.replace('.py','')}_tx"
                                    tx_command = f"{entry.name.replace('.py','')}_tx(trans)"
                                    exec (import_command)
                                    exec (tx_command)


        
    def consensus_raund_1(self):
        if not self.raund_1_node:
              dprint("Raund 1: in get candidate blocks\n")
              from node.unl import get_as_node_type
              from node.myownp2pn import mynode


              
              mynode.main_node.send_my_block(get_as_node_type(self.total_validators))
              self.raund_1_node = True
              self.save_block()

        if len(self.candidate_blocks) > ((len(self.total_validators) * 80)/100) or not (int(time.time()) - self.raund_1_starting_time) < self.raund_1_time:
          temp_validating_list = []
          dprint("Raund 1: first ok")
          dprint(len(self.candidate_blocks))
          for candidate_block in self.candidate_blocks[:]:


              for other_block_tx in candidate_block["transaction"]:

                  tx_valid = 1

                  for my_txs in self.validating_list:
                      if other_block_tx.signature == my_txs.signature:
                          tx_valid += 1


                  if len(self.candidate_blocks) != 1:
                      dprint("Raund 1: Test tx")
                      for other_block in self.candidate_blocks[:]:
                        if candidate_block["signature"] != other_block["signature"]:
                            dprint("Raund 1: Test tx 2")
                            for other_block_txs in other_block["transaction"]:
                                if other_block_tx.signature == other_block_txs.signature:
                                    dprint("Raund 1: Test tx 3")
                                    tx_valid += 1
                  else:
                      tx_valid += 1


                  if tx_valid > (len(self.total_validators) / 2):
                      dprint("Raund 1: second ok")
                      already_in_ok = False
                      for alrady_tx  in temp_validating_list[:]:
                          
                          if other_block_tx.signature == alrady_tx.signature:
                              already_in_ok = True
                      if not already_in_ok:
                            dprint("Raund 1: third ok")
                            temp_validating_list.append(other_block_tx)





          for my_validating_list in self.validating_list[:]:
              ok = False
              for my_temp_validating_list in temp_validating_list[:]:
                  if my_validating_list.signature == my_temp_validating_list.signature:
                      ok = True
              self.validating_list.remove(my_validating_list) 
              if not ok:
                self.createTrans(my_validating_list.sequance_number, my_validating_list.signature, my_validating_list.fromUser, my_validating_list.toUser, my_validating_list.transaction_fee, my_validating_list.data, my_validating_list.amount, transaction_sender = None)
                

                
          self.validating_list = temp_validating_list      


          self.raund_1 = True

          self.raund_2_starting_time = int(time.time())

          



          self.proccess_the_transaction()


          self.calculate_hash()



          self.save_block()





          dprint("Raund 1: self.validating_list: ")
          for element_3 in self.validating_list:
            dprint(str(element_3.__dict__))
            

    def reset_the_block(self):
        
        dprint("""\n
  _____                          _     ____  _      ____   _____ _  __
 / ____|                        | |   |  _ \| |    / __ \ / ____| |/ /
| |    _   _ _ __ _ __ ___ _ __ | |_  | |_) | |   | |  | | |    | ' / 
| |   | | | | '__| '__/ _ \ '_ \| __| |  _ <| |   | |  | | |    |  <  
| |___| |_| | |  | | |  __/ | | | |_  | |_) | |___| |__| | |____| . \ 
 \_____\__,_|_|  |_|  \___|_| |_|\__| |____/|______\____/ \_____|_|\_\
                                        
        """+str(self.__dict__)+"\n")

        self.app_tigger()


        self.previous_hash = self.hash
        self.sequance_number = self.sequance_number + 1
        self.validating_list = []
        self.validating_list_starting_time = int(time.time())
        
        self.hash = None

        self.candidate_blocks = []
        self.candidate_block_hashes = []





        self.raund_1_starting_time = None
        self.raund_1 = False
        self.raund_1_node = False
        
        self.raund_2_starting_time = None
        self.raund_2 = False
        self.raund_2_node = False


        self.validated = False

        self.save_block()


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


    def consensus_raund_2(self):
        if not self.raund_2_node:
              dprint("Raund 2: in get candidate block hashes\n")
              from node.unl import get_as_node_type
              from node.myownp2pn import mynode


              

              mynode.main_node.send_my_block_hash(get_as_node_type(self.total_validators))
              self.raund_2_node = True
              self.save_block()

        if len(self.candidate_block_hashes) > ((len(self.total_validators) * 80)/100) or not (int(time.time()) - self.raund_2_starting_time) < self.raund_2_time:
          temp_validating_list = []
          dprint("Raund 2: first ok")
          for candidate_block in self.candidate_block_hashes[:]:
                  tx_valid = 1

                  if self.hash == candidate_block["hash"]:
                      tx_valid += 1


                  for other_block in self.candidate_block_hashes[:]:

                    if candidate_block != other_block:
                        if candidate_block["hash"] == other_block["hash"]:
                            tx_valid += 1

                  if tx_valid > ((len(self.total_validators) * 80)/100):
                      
                      dprint("Raund 2: second ok")
                      if self.hash == candidate_block["hash"]:
                        self.validated = True
                        

                        
                        
                      else:
                          print("Raund 2: my block is not valid")
                          from node.myownp2pn import mynode
                          from node.unl import get_unl_nodes, get_as_node_type
                          node = mynode.main_node
                          unl_list = get_as_node_type([candidate_block["sender"]])
                          node.send_data_to_node(unl_list[0], "sendmefullblock")
                          self.dowload_true_block = candidate_block["sender"]
                          self.save_block()

                          


        
          if self.validated:
           self.raund_2 = True


           self.reset_the_block()

          



           dprint("Raund 2: self.validating_list: ")
           for element_3 in self.validating_list:
             dprint(str(element_3.__dict__))
            



    def Verificate_Pending_Trans(self):
        dprint("Pending transactions number: "+str(len(self.pendingTransaction)))
        dprint("Validating transactions number: "+str(len(self.validating_list)))
        print(self.raund_1_starting_time)
        if len(self.validating_list) < self.max_tx_number and self.raund_1_starting_time == None:
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
        from lib.config_system import get_config
        import os


        os.chdir(get_config()["main_folder"])
        with open(TEMP_BLOCK_PATH, 'wb') as block_file:
            pickle.dump(self, block_file, protocol=2)









def get_block():
    from lib.config_system import get_config
    import os

    os.chdir(get_config()["main_folder"])
    with open(TEMP_BLOCK_PATH, 'rb') as block_file:
        return pickle.load(block_file)



def sendme_full_node_list():
    from node.myownp2pn import mynode
    from node.unl import get_unl_nodes, get_as_node_type
    node = mynode.main_node
    unl_list = get_as_node_type(get_unl_nodes())
    node.send_data_to_node(unl_list[0], "sendmefullnodelist")


def get_block_from_other_node():
    from node.myownp2pn import mynode
    from node.unl import get_unl_nodes, get_as_node_type
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
        system = Block(0,pubkey)
        from node.myownp2pn import mynode
        mynode.main_node.send_full_chain()
    else:
        dprint("Getting block from nodes")
        get_block()
