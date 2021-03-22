import pickle

from lib.mixlib import dprint

def save_new_unl_node(id):
    id = id.replace('\n', '')
    node = None

    from node.myownp2pn import MyOwnPeer2PeerNode
    for inbound_node in MyOwnPeer2PeerNode.main_node.nodes_inbound:
        if id in (inbound_node.id).replace('\n', ''):
            node = inbound_node
    for outbound_node in MyOwnPeer2PeerNode.main_node.nodes_outbound:
        if id in (outbound_node.id).replace('\n', ''):
            node = outbound_node
    if node != None:
        nodes_list = get_unl_nodes()

        already_in_list = False

        for element in nodes_list:
            if element == node.id:
                already_in_list = True

        if not already_in_list:

     
         nodes_list.append(node.id)

         
         import os
         import sys
         sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
         from config import get_config
         old_cwd = os.getcwd()
         os.chdir(get_config().main_folder)
         with open('unl_nodes.decentra_network', 'wb') as unl_nodes_file:
             pickle.dump(nodes_list, unl_nodes_file)
         os.chdir(old_cwd)

def get_unl_nodes():
        try:
         import os
         import sys
         sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
         from config import get_config
         old_cwd = os.getcwd()
         os.chdir(get_config().main_folder)
         with open('unl_nodes.decentra_network', 'rb') as unl_nodes_file:
             nodes_list = pickle.load(unl_nodes_file)
         os.chdir(old_cwd)

        except:
            nodes_list = [] 
        return nodes_list

def get_as_node_type(id_list):
        dprint(id_list)
        temp_list = []
        from node.myownp2pn import MyOwnPeer2PeerNode
        for list_node in id_list:
            for inbound in MyOwnPeer2PeerNode.main_node.nodes_inbound:
                if list_node in inbound.id:
                    temp_list.append(inbound)
            for outbound in MyOwnPeer2PeerNode.main_node.nodes_outbound:
                if list_node in outbound.id:
                    temp_list.append(outbound)
        return temp_list


def node_is_unl(node_id):
    node_id = node_id.replace('\n', '')
    for unl in get_unl_nodes():
        temp_unl = unl.replace('\n', '')
        if node_id in temp_unl:
            return True
    return False