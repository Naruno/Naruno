#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from node.node import *

from wallet.wallet import Signature , Ecdsa , PublicKey , PrivateKey , Wallet_Import

from lib.mixlib import dprint

from hashlib import sha256

from lib.merkle_root import MerkleTree

from transactions.transaction import Transaction



import os

from config import TEMP_BLOCK_PATH, LOADING_BLOCK_PATH, TEMP_ACCOUNTS_PATH, TEMP_BLOCKSHASH_PATH

from blockchain.block.get_block import GetBlock

class mynode (Node):
    main_node = None
    unl_nodes = []

    def __init__(self, host, port):
        self.__class__.main_node = self
        super(mynode, self).__init__(host, port, None)
        print("MyPeer2PeerNode: Started")



    def message_from_node(self, node, data):
        from node.unl import get_unl_nodes, get_as_node_type
    
        if str(data) == "sendmefullblock":
            self.send_full_chain(node)
        print("Data Type: "+str(type(data))+"\n")


        try:
            from node.unl import node_is_unl
            if data["fullblock"] == 1 and node_is_unl(node.id) and Ecdsa.verify("fullblock"+data["byte"], Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                print("getting chain")
                self.get_full_chain(data,node)
        except Exception as e:
            print(e)

        try:
            from node.unl import node_is_unl
            if data["fullaccounts"] == 1 and node_is_unl(node.id) and Ecdsa.verify("fullaccounts"+data["byte"], Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                print("getting chain")
                self.get_full_accounts(data,node)
        except Exception as e:
            print(e)

        try:
            from node.unl import node_is_unl
            if data["fullblockshash"] == 1 and node_is_unl(node.id) and Ecdsa.verify("fullblockshash"+data["byte"], Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                self.get_full_blockshash(data,node)
        except Exception as e:
            print(e)

        try:
         if data["transactionrequest"]  == 1:
            self.get_transaction(data,node)
        except Exception as e:
            print(e)



            
        try:
         if data["action"]  == "myblock":
            self.get_candidate_block(data,node)
        except Exception as e:
            print(e)




        try:
         if data["action"]  == "myblockhash":
            self.get_candidate_block_hash(data,node)
        except Exception as e:
            print(e)


        print("message_from_node from " + node.id + ": " + str(data))
        
    def node_disconnect_to_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")




    def send_my_block(self,nodes):
         system = GetBlock()

         new_list = []

         signature_list = []

         for element in system.validating_list:
             new_list.append(element.dump_json())
             signature_list.append(element.signature)

         dprint("signature_list: "+str(signature_list))
         dprint("publickey from pem: "+str(Wallet_Import(0,1)))


         Merkle_signature_list = MerkleTree(signature_list).getRootHash() if len(signature_list) != 0 else "0"


         dprint("\nmerkleroot: "+Merkle_signature_list)

         data = {
             "action":"myblock",
             "transaction": new_list,
             "sequance_number": system.sequance_number,
             "signature":Ecdsa.sign("myblock"+Merkle_signature_list+str(system.sequance_number), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()
         }

         for each_node in nodes:
            dprint("Raund 1: second ok of get candidate block: "+ str(each_node.__dict__))
            self.send_data_to_node(each_node,data)

    def send_my_block_hash(self,nodes):
        system = GetBlock()

        if system.raund_1 and not system.raund_2:


         data = {
             "action":"myblockhash",
             "hash": system.hash,
             "sequance_number": system.sequance_number,
             "signature":Ecdsa.sign("myblockhash"+system.hash+str(system.sequance_number), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()
         }

         for each_node in nodes:
             dprint("Raund 2: second ok of get candidate block hashes: "+ str(each_node.__dict__))
             self.send_data_to_node(each_node,data)


    def get_candidate_block(self,data,node):

      dprint("Getting the candidate block")
      from node.unl import node_is_unl
      if node_is_unl(node.id) and GetBlock().sequance_number == data["sequance_number"]:
            dprint("is unl")

            signature_list = []
            for element in data["transaction"]:
                signature_list.append(element["signature"])

            dprint("signature_list: "+str(signature_list))

            merkle_root_of_signature_list = MerkleTree(signature_list).getRootHash() if len(signature_list) != 0 else "0"


            

            dprint("signatureverify: "+str(Ecdsa.verify("myblock"+merkle_root_of_signature_list, Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id))))
            dprint("publickey from pem: "+str(node.id))
            
            dprint("merkleroot: "+merkle_root_of_signature_list)

            if Ecdsa.verify("myblock"+merkle_root_of_signature_list+str(data["sequance_number"]), Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                dprint("ecdsa true")

                temp_tx = []

                for element in data["transaction"]:
                    temp_tx.append(Transaction.load_json(element))

                data["transaction"] = temp_tx

                node.candidate_block = data


    def get_candidate_block_hash(self,data,node):

      dprint("Getting the candidate block hash")

      from node.unl import node_is_unl
      if node_is_unl(node.id) and GetBlock().sequance_number == data["sequance_number"]:
            dprint("is unl")


            if Ecdsa.verify("myblockhash"+data["hash"]+str(data["sequance_number"]), Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                dprint("ecdsa true")
                data["sender"] = node.id

                node.candidate_block_hash = data



    def send_full_chain(self,node = None):
        dprint("Sending full chain to node or nodes."+" Node: "+ str(node))
        file = open(TEMP_BLOCK_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {"fullblock" : 1,"byte" : (SendData.decode(encoding='iso-8859-1')),"signature" : Ecdsa.sign("fullblock"+str((SendData.decode(encoding='iso-8859-1'))), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
            if not node is None:
                self.send_data_to_node(node,data)
            else:
                self.send_data_to_nodes(data)

            SendData = file.read(1024) 

            dprint(SendData)

            if not SendData:
                data = {"fullblock" : 1,"byte" : "end","signature": Ecdsa.sign("fullblock"+"end", PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
                if not node is None:
                    self.send_data_to_node(node,data)
                else:
                    self.send_data_to_nodes(data)


    def send_full_accounts(self,node = None):
        dprint("Sending full chain to node or nodes."+" Node: "+ str(node))
        file = open(TEMP_ACCOUNTS_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {"fullaccounts" : 1,"byte" : (SendData.decode(encoding='iso-8859-1')),"signature" : Ecdsa.sign("fullaccounts"+str((SendData.decode(encoding='iso-8859-1'))), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
            if not node is None:
                self.send_data_to_node(node,data)
            else:
                self.send_data_to_nodes(data)

            SendData = file.read(1024) 

            dprint(SendData)

            if not SendData:
                data = {"fullaccounts" : 1,"byte" : "end","signature": Ecdsa.sign("fullaccounts"+"end", PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
                if not node is None:
                    self.send_data_to_node(node,data)
                else:
                    self.send_data_to_nodes(data)

    def send_full_blockshash(self,node = None):
        dprint("Sending full chain to node or nodes."+" Node: "+ str(node))
        file = open(TEMP_BLOCKSHASH_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {"fullblockshash" : 1,"byte" : (SendData.decode(encoding='iso-8859-1')),"signature" : Ecdsa.sign("fullblockshash"+str((SendData.decode(encoding='iso-8859-1'))), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
            if not node is None:
                self.send_data_to_node(node,data)
            else:
                self.send_data_to_nodes(data)

            SendData = file.read(1024) 

            dprint(SendData)

            if not SendData:
                data = {"fullblockshash" : 1,"byte" : "end","signature": Ecdsa.sign("fullblockshash"+"end", PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
                if not node is None:
                    self.send_data_to_node(node,data)
                else:
                    self.send_data_to_nodes(data)


    def get_full_chain(self,data,node):
      
      get_ok = False

      if not os.path.exists(TEMP_BLOCK_PATH):
        get_ok = True
      else:
        system = GetBlock()
        if node.id == system.dowload_true_block:
            get_ok = True

      
      if get_ok:



        if str(data["byte"]) == "end":

            os.rename(LOADING_BLOCK_PATH, TEMP_BLOCK_PATH)
            
            from blockchain.block.block_main import apps_starter
            from consensus.consensus_main import consensus_trigger
            from lib.perpetualtimer import perpetualTimer
            from app.app_main import apps_starter
            system = GetBlock()
            system.newly = True
            from transactions.change_transaction_fee import ChangeTransactionFee
            ChangeTransactionFee(system)

            system.exclude_validators = []
            dprint(system.sequance_number)
            perpetualTimer(system.consensus_timer,consensus_trigger).start()
            apps_starter()
            system.save_block()
            


        else:
            file = open(LOADING_BLOCK_PATH, "ab")
                
            file.write((data["byte"].encode(encoding='iso-8859-1')))
            file.close()


    def get_full_blockshash(self,data,node):
      
      get_ok = False

      if not os.path.exists(TEMP_BLOCKSHASH_PATH):
        get_ok = True
      else:
        system = GetBlock()
        if node.id == system.dowload_true_block:
            get_ok = True

      
      if get_ok:
        file = open(TEMP_BLOCKSHASH_PATH, "ab")
                
        file.write((data["byte"].encode(encoding='iso-8859-1')))
        file.close()

    def get_full_accounts(self,data,node):
      
      get_ok = False

      if not os.path.exists(TEMP_ACCOUNTS_PATH):
        get_ok = True
      else:
        system = GetBlock()
        if node.id == system.dowload_true_block:
            get_ok = True

      
      if get_ok:
        file = open(TEMP_ACCOUNTS_PATH, "ab")
                
        file.write((data["byte"].encode(encoding='iso-8859-1')))
        file.close()



    def get_transaction(self,data,node):
        dprint("Getting the transactions")
        system = GetBlock()
        from transactions.create_transaction import CreateTransaction
        CreateTransaction(system, sequance_number = data["sequance_number"],signature =data["signature"],fromUser = data["fromUser"],toUser = data["to_user"],data = data["data"],amount = data["amount"],transaction_fee = data["transaction_fee"],transaction_sender=node, transaction_time = data["transaction_time"])
