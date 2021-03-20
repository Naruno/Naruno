import datetime
import hashlib

import pprint

from wallet.wallet import Ecdsa , PrivateKey , PublicKey , Wallet_Import , Signature

import pickle


from ledger.merkleroot import mixmerkletree


from lib.settings import the_settings
from lib.mixlib import dprint

import os

class Account:
    def __init__(self, PublicKey,balance):
        self.PublicKey = PublicKey
        self.sequance_number = 0
        self.balance = balance
 
class ledger:
    def __init__(self,creator):
        self.Accounts = [Account(creator,balance=1000000)]
        self.pendingTransaction = []
        self.validating_list = []
        self.save_ledger()




 

    def minePendingTrans(self):
        dprint("Pending transactions number: "+str(len(self.pendingTransaction)))
        dprint("Validating transactions number: "+str(len(self.validating_list)))
        if len(self.pendingTransaction) > 2 and not len(self.validating_list) > 2:
          for tx in self.pendingTransaction:
              self.validating_list.append(tx)
          self.pendingTransaction.clear()


        for trans in self.validating_list:
          dprint("Transaction")
          if self.tx_verification(trans) == True:

            dprint("tx_verification true")
            touser_inlist = False
            for Accounts in self.Accounts:
                dprint("Accounts")
                if trans.fromUser in Accounts.PublicKey:
                    dprint("Sender")
                    Accounts.balance -= (float(trans.amount)+trans.transaction_fee)
                    Accounts.sequance_number += 1
                elif trans.toUser in Accounts.PublicKey:
                    dprint("Touser")
                    Accounts.balance += float(trans.amount)
                    touser_inlist = True
            if touser_inlist == False:
                self.Accounts.append(Account(trans.toUser,float(trans.amount)))
            self.validating_list.remove(trans)


            for folder_entry in os.scandir('apps'):
             if not ".md" in folder_entry.name:
              for entry in os.scandir("apps/"+folder_entry.name):
                if entry.is_file():
                    if entry.name[0] != '_' and ".py" in entry.name and "_main" in entry.name:
                        import_command = f"from apps.{folder_entry.name}.{entry.name.replace('.py','')} import {entry.name.replace('.py','')}_tx" 
                        tx_command = f"{entry.name.replace('.py','')}_tx(trans)"
                        dprint(import_command)
                        exec (import_command)
                        dprint(tx_command)
                        exec (tx_command)

        dprint("End mining pending transactions number: "+str(len(self.pendingTransaction)))
        dprint("End mining validating transactions number: "+str(len(self.validating_list)))

 
        self.save_ledger()


    def tx_verification(self,tx):
        if len(tx.valid) >= (len(tx.total_validators) / 3):
            dprint("tx_verification okey")
            return True
        else:
            if (len(tx.valid) + len(tx.invalid)) != len(tx.total_validators):
             dprint("sending response request to unl nodes")
             #burda sadece istediğimiz daha doğrusu unl listemizdeki adamlara mesaj atacağız. ayrıca valid veya invalid kararını vermemişlere atacağız sadece
             from node.myownp2pn import MyOwnPeer2PeerNode
             exclude_list = []
             dprint("tx_valid_in ledger"+str(tx.valid))
             dprint("tx_invalid_in ledger"+str(tx.invalid))
             for validators in tx.valid:
                 dprint("validators_in ledger"+str(validators))
                 exclude_list.append(validators["node"])
             for invalidators in tx.invalid:
                 dprint("invalidators_in ledger"+str(invalidators))
                 exclude_list.append(invalidators["node"])
             for already_asked in tx.already_asked_nodes:
                 exclude_list.append(already_asked)

             dprint("exclude list_in ledger"+str(exclude_list))
             from node.unl import get_as_node_type
             nodes_list = get_as_node_type(tx.total_validators)
             dprint("Nodes list: "+str(nodes_list))
             for node in nodes_list:
                 if not node in get_as_node_type(exclude_list):
                    tx.already_asked_nodes.append(node.id)
                    MyOwnPeer2PeerNode.main_node.send_to_node(node,{"transactionrequest" : 1,"sequance_number": tx.sequance_number, "signature" : tx.signature, "fromUser" : tx.fromUser , "to_user" : tx.toUser, "data" : tx.data, "amount" : tx.amount,"transaction_fee":tx.transaction_fee,"response":True})


            return False

    def createTrans(self,sequance_number,signature, fromUser,toUser,transaction_fee,data = None, amount = None,transaction_sender = None,response = False):

      dprint("Creating transaction.")
      signature_class = Signature.fromBase64(signature)
      dprint("***")
      dprint(sequance_number)
      dprint(signature)
      dprint(fromUser)
      dprint(toUser)
      dprint(data)
      dprint(amount)
      dprint("***")
      dprint(Ecdsa.verify((str(sequance_number)+str(fromUser)+str(toUser)+str(data)+str(amount)+str(transaction_fee)), signature_class, PublicKey.fromPem(fromUser)))
      
      temp_signature = signature_class.toBase64()
      already_in_pending = False
      for pendingtx in self.pendingTransaction:
          if pendingtx.signature == temp_signature:
              already_in_pending = True
      for validatingtx in self.validating_list:
          if validatingtx.signature == temp_signature:
              already_in_pending = True
      if Ecdsa.verify((str(sequance_number)+str(fromUser)+str(toUser)+str(data)+str(amount)+str(transaction_fee)), signature_class, PublicKey.fromPem(fromUser)) and (sequance_number == (self.getSequanceNumber(fromUser)+1) or already_in_pending):
          dprint("Sign verify is true.")
          if (self.getBalance(fromUser) >= (float(amount)+float(transaction_fee)) and float(amount) != float(0)) or response == False: #burası sadece response true ise değerlendirilecek şekilde yenilenebilir
               temp_transaction = Transaction(sequance_number=sequance_number,signature=signature_class.toBase64(),fromUser=fromUser,toUser=toUser,data = data,amount = amount,transaction_fee = transaction_fee)
               dprint("Balance controll is true.")
               if already_in_pending == False:
                   self.pendingTransaction.append(temp_transaction)
                   self.save_ledger()
               dprint("already pending 1")
               from node.myownp2pn import MyOwnPeer2PeerNode
               dprint("imported myownpeer2peernode")
               if transaction_sender == None:
                   dprint("not node coming")
                   if already_in_pending == False:
                       MyOwnPeer2PeerNode.main_node.send_to_nodes({"transactionrequest" : 1,"sequance_number": sequance_number, "signature" : signature, "fromUser" : fromUser , "to_user" : toUser, "data" : data, "amount" : amount,"transaction_fee":transaction_fee,"response":False})
               else:
                   dprint("node coming")
                   dprint(str(response))
                   if response == True:
                       dprint("response true")
                       self.send_my_response_on_transaction(temp_transaction = temp_transaction,response="TRUE",transaction_sender=transaction_sender)
                   if already_in_pending == False:
                       MyOwnPeer2PeerNode.main_node.send_to_nodes({"transactionrequest" : 1,"sequance_number": sequance_number, "signature" : signature, "fromUser" : fromUser , "to_user" : toUser, "data" : data, "amount" : amount,"transaction_fee":transaction_fee,"response":False},exclude=[transaction_sender])
               #if already_in_pending == False: #burası sanırım olmamamlı çöünkü olduğu zaman karşı taraf bu sorgulandığı zaman herhangi bir tepki vermiyor burdan dolayı yani sorgulandığı zamanda bence gönderen node harici diğer nodelara gönderim sağlanacak şekilde istekler oluşturulabilir.
               self.minePendingTrans()
               return True
          else:
              if transaction_sender != None and response == True:
                  self.send_my_response_on_transaction(temp_transaction = temp_transaction,response="FALSE",transaction_sender=transaction_sender)
      else:
         dprint("verify false")
         dprint(response)
         dprint(transaction_sender)
         if transaction_sender != None and response == True:
             self.send_my_response_on_transaction(temp_transaction = temp_transaction,response="FALSE",transaction_sender=transaction_sender)
    def send_my_response_on_transaction(self,temp_transaction,response,transaction_sender):
        dprint("sending the response")
        dprint(response)
        from node.myownp2pn import MyOwnPeer2PeerNode
        MyOwnPeer2PeerNode.main_node.send_to_node(transaction_sender,{"transactionresponse" : 1,"fromUser":MyOwnPeer2PeerNode.main_node.id,"response":response,"transaction_signature" : temp_transaction.signature,"signature": Ecdsa.sign(response+str(temp_transaction.signature), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()})
 

 
    def getBalance(self,user):
        balance = 0
        for Accounts in self.Accounts:
            if user in Accounts.PublicKey:
                balance = Accounts.balance
                for trans in self.pendingTransaction:
                    for Accounts in self.Accounts:
                        if trans.fromUser in Accounts.PublicKey:
                            balance -= (float(trans.amount)-trans.transaction_fee)
                        elif trans.toUser in Accounts.PublicKey:
                            balance += float(trans.amount)
                return balance
        return balance
    def getSequanceNumber(self,user):
        sequance_number = 0
        for Accounts in self.Accounts:
            if user in Accounts.PublicKey:
                sequance_number = Accounts.sequance_number
                for trans in self.pendingTransaction:
                    for Accounts in self.Accounts:
                        if trans.fromUser in Accounts.PublicKey:
                            sequance_number += 1
                return sequance_number
        return sequance_number

    def save_ledger(self):
        from config import get_config
        import os
        old_cwd = os.getcwd()
        os.chdir(get_config().main_folder)
        with open('ledger.decentra_network', 'wb') as ledger_file:
            pickle.dump(self, ledger_file,protocol=2)
        os.chdir(old_cwd)

 
 
class Transaction:
    def __init__(self,sequance_number,signature,fromUser,toUser,data,amount,transaction_fee):
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
        from config import get_config
        import os
        old_cwd = os.getcwd()
        os.chdir(get_config().main_folder)
        with open('ledger.decentra_network', 'rb') as ledger_file:
            return pickle.load(ledger_file)
        os.chdir(old_cwd)




def sendme_full_node_list():
    from node.myownp2pn import MyOwnPeer2PeerNode
    node = MyOwnPeer2PeerNode.main_node
    node.send_to_node(node.nodes_outbound[0],"sendmefullnodelist")  


def get_ledger():
    from node.myownp2pn import MyOwnPeer2PeerNode
    node = MyOwnPeer2PeerNode.main_node
    try:
        node.send_to_node(node.nodes_outbound[0],"sendmefullledger")   
    except:
        pass
    try:
        node.send_to_node(node.nodes_inbound[0],"sendmefullledger")   
    except:
        pass

def create_ledger():
    
    if the_settings().test_mode() == True:
        dprint("Creating new ledger")
        system = ledger(Wallet_Import(0,0))
        from node.myownp2pn import MyOwnPeer2PeerNode
        MyOwnPeer2PeerNode.main_node.send_full_chain()
    else:
        dprint("Getting ledger from nodes")
        get_ledger()