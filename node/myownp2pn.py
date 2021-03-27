#https://github.com/macsnoeren/python-p2p-network was used for infrastructure

from node.node import *
import pickle

from wallet.wallet import Signature , Ecdsa , PublicKey , PrivateKey , Wallet_Import

from lib.mixlib import dprint




class MyOwnPeer2PeerNode (Node):
    main_node = None
    unl_nodes = []
    # Python class constructor
    def __init__(self, host, port):
        self.__class__.main_node = self
        super(MyOwnPeer2PeerNode, self).__init__(host, port, None)
        print("MyPeer2PeerNode: Started")


    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        print("outbound_node_connected: " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: " + node.id)

    def inbound_node_disconnected(self, node):
      
        print("inbound_node_disconnected: " + node.id)

    def outbound_node_disconnected(self, node):
        
        print("outbound_node_disconnected: " + node.id)

    def node_message(self, node, data):
        from node.unl import get_unl_nodes, get_as_node_type
    
        if str(data) == "sendmefullledger":
            self.send_full_chain(node)
        print("Data Type: "+str(type(data))+"\n")

        if str(data) == "sendmefullnodelist":
            self.send_full_node_list(node)
        print("Data Type: "+str(type(data))+"\n")

        try:
            from node.unl import node_is_unl
            if data["fullledger"] == 1 and node_is_unl(node.id) and Ecdsa.verify("fullledger"+data["byte"], Signature.fromBase64(data["signature"]), PublicKey.fromPem(node.id)):
                print("getting chain")
                self.get_full_chain(data["byte"])
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
         if data["transactionresponse"]  == 1:
            self.get_transaction_response(data,node)
        except Exception as e:
            print(e)
            pass

        print("node_message from " + node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    def send_full_chain(self,node = None):
        from config import LEDGER_PATH
        dprint("Sending full chain to node or nodes."+" Node: "+ str(node))
        file = open(LEDGER_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {"fullledger" : 1,"byte" : (SendData.decode(encoding='iso-8859-1')),"signature" : Ecdsa.sign("fullledger"+str((SendData.decode(encoding='iso-8859-1'))), PrivateKey.fromPem(Wallet_Import(0,1))).toBase64()}
            if not node == None:
                self.send_to_node(node,data)
            else:
                self.send_to_nodes(data)

            SendData = file.read(1024) 
    def get_full_chain(self,data):
        from config import LEDGER_PATH
        file = open(LEDGER_PATH, "ab")

        file.write((data.encode(encoding='iso-8859-1')))

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
                self.send_to_node(node,data)
            else:
                self.send_to_nodes(data)

            SendData = file.read(1024) 
    def get_full_node_list(self,data):
        from config import CONNECTED_NODE_PATH
        file = open(CONNECTED_NODE_PATH, "ab")

        file.write((data.encode(encoding='iso-8859-1')))

        file.close()


    def get_transaction(self,data,node):
        from ledger.ledger_main import get_ledger
        dprint("Getting the transactions")
        system = get_ledger()
        system.createTrans(sequance_number = data["sequance_number"],signature =data["signature"],fromUser = data["fromUser"],toUser = data["to_user"],data = data["data"],amount = data["amount"],transaction_fee = data["transaction_fee"],transaction_sender=node,response=data["response"])
        system.Verificate_Pending_Trans(Wallet_Import(0,0))


    def get_transaction_response(self,data,node):
      #burada bu mesaj gönderen adamın bizim istediğimiz node ve pub key olup olmadığına bakacağız. ayrıca eğer unl listemizdeki bir adamdan evet oyu aldıysak o oyu hayıra çeviremeyiz
      from ledger.ledger_main import get_ledger
      dprint("Getting the transactions response")
      system = get_ledger()
      from node.unl import node_is_unl
      if node_is_unl(node.id):
        for tx in system.validating_list:

            if node.id in data["fromUser"] and Ecdsa.verify(data["response"]+str(data["transaction_signature"]), Signature.fromBase64(data["signature"]), PublicKey.fromPem(data["fromUser"])):

                if data["transaction_signature"] == tx.signature:
                    if data["response"] == "TRUE":
                        tx.valid.append({"data":data,"node":node.id})
                        system.Verificate_Pending_Trans()
                    elif data["response"] == "FALSE":
                        tx.invalid.append({"data":data,"node":node.id})
                        system.Verificate_Pending_Trans()