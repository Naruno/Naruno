from node.myownp2pn import MyOwnPeer2PeerNode
from lib.settings import the_settings


def ndstart(ip,port):
    node = MyOwnPeer2PeerNode(ip,port)
    #node.debug = the_settings().debug_mode()
    node.start()     

def ndstop():
    MyOwnPeer2PeerNode.main_node.stop()

def ndconnect(ip,port):
    MyOwnPeer2PeerNode.main_node.connect_with_node(ip, port)


def ndconnectmixdb():
    MyOwnPeer2PeerNode.main_node.connectionfrommixdb()