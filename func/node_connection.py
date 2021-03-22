from node.myownp2pn import MyOwnPeer2PeerNode, connectionfrommixdb
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
    connectionfrommixdb()

def connect_to_main_network():
    import requests
    
    url = 'https://raw.githubusercontent.com/onuratakan/Decentra-Network/master/connected_node.decentra_network'
    r = requests.get(url, allow_redirects=True)
    open('connected_node.decentra_network', 'wb').write(r.content)  

    ndconnectmixdb()