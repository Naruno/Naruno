#!/usr/bin/python3
# -*- coding: utf-8 -*-

from node.node import *
import pickle

from wallet.wallet import Signature , Ecdsa , PublicKey , PrivateKey , Wallet_Import

from lib.mixlib import dprint

from hashlib import sha256


from func.merkle_root import MerkleTree


from blockchain.block.transaction import Transaction

import os


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

        if str(data) == "sendmefullnodelist":
            self.send_full_node_list(node)
        print("Data Type: "+str(type(data))+"\n")

        try:
            from node.unl import node_is_unl
            if data["fullblock"] == 1 and node_is_unl(node.id) and Ecdsa.verify("fullblock"+data["byte"], Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                print("getting chain")
                self.get_full_chain(data)
        except:
            pass

        try:
            from node.unl import node_is_unl
            if data["fullnodelist"] == 1 and node_is_unl(node.id) and Ecdsa.verify("fullnodelist"+data["byte"], Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                print("getting node list")
                self.get_full_node_list(data["byte"])
        except:
            pass

        try:
         if data["transactionrequest"]  == 1:
            self.get_transaction(data,node)
        except Exception as e:
            print(e)
            pass


        try:
         if data["action"]  == "sendmeyourblock":
            self.send_my_block(node)
        except Exception as e:
            print(e)
            pass
        try:
         if data["action"]  == "myblock":
            self.get_candidate_block(data,node)
        except Exception as e:
            print(e)
            pass

        try:
         if data["action"]  == "sendmeyourblockhash":
            self.send_my_block_hash(node)
        except Exception as e:
            print(e)
            pass
        try:
         if data["action"]  == "myblockhash":
            self.get_candidate_block_hash(data,node)
        except Exception as e:
            print(e)
            pass

        print("message_from_node from " + node.id + ": " + str(data))
        
    def node_disconnect_to_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")




    def send_my_block(self,node):
        from blockchain.block.block_main import get_block
        system = get_block()

        if not len(system.validating_list) < system.max_tx_number:
         new_list = []

         signature_list = []

         for element in system.validating_list:
             new_list.append(element.dump_json())
             signature_list.append(element.signature)

         dprint("signature_list: "+str(signature_list))
         dprint("publickey from pem: "+str(Wallet_Import(0,1)))

         dprint("\nmerkleroot: "+str(MerkleTree(signature_list).getRootHash()))

         data = {
             "action":"myblock",
             "transaction": new_list,
             "signature":Ecdsa.sign("myblock"+str(MerkleTree(signature_list).getRootHash()), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()
         }
         self.send_data_to_node(node,data)

    def send_my_block_hash(self,node):
        from blockchain.block.block_main import get_block
        system = get_block()

        if system.raund_1 and system.raund_2 != True:


         data = {
             "action":"myblockhash",
             "hash": system.hash,
             "signature":Ecdsa.sign("myblockhash"+system.hash, PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()
         }
         self.send_data_to_node(node,data)


    def get_candidate_block(self,data,node):

      from blockchain.block.block_main import get_block
      dprint("Getting the candidate block")
      system = get_block()
      from node.unl import node_is_unl
      if node_is_unl(node.id):
            dprint("is unl")

            signature_list = []
            for element in data["transaction"]:
                signature_list.append(element["signature"])

            dprint("signature_list: "+str(signature_list))

            dprint("signatureverify: "+str(Ecdsa.verify("myblock"+str(MerkleTree(signature_list).getRootHash()), Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id))))
            dprint("publickey from pem: "+str(node.id))
            
            dprint("\nmerkleroot: "+str(MerkleTree(signature_list).getRootHash()))

            if Ecdsa.verify("myblock"+str(MerkleTree(signature_list).getRootHash()), Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                dprint("ecdsa true")

                temp_tx = []

                for element in data["transaction"]:
                    temp_tx.append(Transaction.load_json(element))

                data["transaction"] = temp_tx
                
                system.candidate_blocks.append(data)
                system.save_block()


    def get_candidate_block_hash(self,data,node):

      from blockchain.block.block_main import get_block
      dprint("Getting the candidate block hash")
      system = get_block()
      from node.unl import node_is_unl
      if node_is_unl(node.id):
            dprint("is unl")


            if Ecdsa.verify("myblockhash"+data["hash"], Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                dprint("ecdsa true")

                
                system.candidate_block_hashes.append(data)
                system.save_block()



    def send_full_chain(self,node = None):
        from config import TEMP_BLOCK_PATH
        dprint("Sending full chain to node or nodes."+" Node: "+ str(node))
        file = open(TEMP_BLOCK_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {"fullblock" : 1,"byte" : (SendData.decode(encoding='iso-8859-1')),"signature" : Ecdsa.sign("fullblock"+str((SendData.decode(encoding='iso-8859-1'))), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
            if not node == None:
                self.send_data_to_node(node,data)
            else:
                self.send_data_to_nodes(data)

            SendData = file.read(1024) 

            dprint(SendData)

            if not SendData:
                data = {"fullblock" : 1,"byte" : "end","signature": Ecdsa.sign("fullblock"+"end", PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
                if not node == None:
                    self.send_data_to_node(node,data)
                else:
                    self.send_data_to_nodes(data)

    def get_full_chain(self,data):
      from config import TEMP_BLOCK_PATH
      import os
      if not os.path.exists(TEMP_BLOCK_PATH):

        if str(data["byte"]) == "end":
            from config import LOADING_BLOCK_PATH, TEMP_BLOCK_PATH


            
            os.rename(LOADING_BLOCK_PATH, TEMP_BLOCK_PATH)

            from blockchain.block.block_main import get_block

            system = get_block()
            
            from node.unl import get_unl_nodes
            system.total_validators = get_unl_nodes()
            system.candidate_blocks = []
            system.exclude_validators = []
            system.save_block()


        else:
            from config import LOADING_BLOCK_PATH
            file = open(LOADING_BLOCK_PATH, "ab")
                
            file.write((data["byte"].encode(encoding='iso-8859-1')))
            file.close()









    def send_full_node_list(self,node = None):
        from config import CONNECTED_NODE_PATH
        file = open(CONNECTED_NODE_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {"fullnodelist" : 1,"byte" : (SendData.decode(encoding='iso-8859-1')),"signature": Ecdsa.sign("fullnodelist"+str((SendData.decode(encoding='iso-8859-1'))), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
            print(data)
            print(type(data))
            if not node == None:
                self.send_data_to_node(node,data)
            else:
                self.send_data_to_nodes(data)

            SendData = file.read(1024)
    def get_full_node_list(self,data):
        from config import CONNECTED_NODE_PATH
        file = open(CONNECTED_NODE_PATH, "ab")

        file.write((data.encode(encoding='iso-8859-1')))

        file.close()


    def get_transaction(self,data,node):
        from blockchain.block.block_main import get_block
        dprint("Getting the transactions")
        system = get_block()
        system.createTrans(sequance_number = data["sequance_number"],signature =data["signature"],fromUser = data["fromUser"],toUser = data["to_user"],data = data["data"],amount = data["amount"],transaction_fee = data["transaction_fee"],transaction_sender=node)
        system.Verificate_Pending_Trans()
