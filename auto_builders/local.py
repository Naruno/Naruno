#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import urllib.request, json
import time
import argparse
import sys
import os
import signal

class Decentra_Network_Local:

    def __init__(self, number_of_nodes = 3, number_of_security_circle = 1):
        self.number_of_nodes = number_of_nodes - 1
        self.number_of_security_circle = number_of_security_circle
    
    def start(self):
        time.sleep(1)
        self.creating_the_wallets()
        self.starting_the_nodest()
        self.unl_nodes_settting()
        self.connecting_the_nodes()
        self.creating_the_block()
        time.sleep(60)

    def install(self):
        os.system("pip3 install -r Decentra-Network/requirements/api.txt")
        os.system(f"cp -r -f Decentra-Network Decentra-Network-0")
        for i in range(self.number_of_nodes):
            os.system(f"cp -r -f Decentra-Network Decentra-Network-{i+1}")

    def delete(self):

        os.system("rm -r -f Decentra-Network-*")      

        for line in os.popen("ps ax | grep python3 | grep -v grep"):
            fields = line.split()
            if "/src/api.py" in fields[5]:
                os.kill(int(fields[0]), signal.SIGKILL)

    def run(self):

        os.system("nohup python3 Decentra-Network-0/src/api.py &")
        for i in range(self.number_of_nodes):
            print(f"nohup python3 Decentra-Network-{i+1}/src/api.py -p 80{i+1}0 &")
            os.system(f"nohup python3 Decentra-Network-{i+1}/src/api.py -p 80{i+1}0 &")

    def creating_the_wallets(self):

        create_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8000/wallet/create/123").read().decode())
        for i in range(self.number_of_nodes):
            create_wallet_2 = json.loads(urllib.request.urlopen(f"http://localhost:80{i+1}0/wallet/create/123").read().decode())

    def starting_the_nodest(self):

        node_start_1 = json.loads(urllib.request.urlopen("http://localhost:8000/node/start/0.0.0.0/7999").read().decode())
        for i in range(self.number_of_nodes):
            node_start_2 = json.loads(urllib.request.urlopen(f"http://localhost:80{i+1}0/node/start/0.0.0.0/800{i+1}").read().decode())

    def unl_nodes_settting(self):

        node_id_1 = json.loads(urllib.request.urlopen("http://localhost:8000/node/id").read().decode())
        for i in range(self.number_of_nodes):
            urllib.request.urlopen(f"http://localhost:80{i+1}0/node/newunl/?{node_id_1}")
        
        if self.number_of_security_circle == 1:
            for i in range(self.number_of_nodes):
                node_id_2 = json.loads(urllib.request.urlopen(f"http://localhost:80{i+1}0/node/id").read().decode())
                urllib.request.urlopen(f"http://localhost:8000/node/newunl/?{node_id_2}")
                for i_n in range(self.number_of_nodes):
                    if not i == i_n:
                        urllib.request.urlopen(f"http://localhost:80{i_n+1}0/node/newunl/?{node_id_2}")
        else:
            nodes_list = list(range(self.number_of_nodes))
            circle_list = [nodes_list[x:x+((self.number_of_nodes+1)//self.number_of_security_circle)] for x in range(0, len(nodes_list), ((self.number_of_nodes+1)//self.number_of_security_circle))]
            for circle in circle_list:
                for i in circle:
                    node_id_2 = json.loads(urllib.request.urlopen(f"http://localhost:80{i+1}0/node/id").read().decode())
                    urllib.request.urlopen(f"http://localhost:8000/node/newunl/?{node_id_2}")                    
                    for i_n in circle:
                        if not i == i_n:
                            urllib.request.urlopen(f"http://localhost:80{i_n+1}0/node/newunl/?{node_id_2}")

    def connecting_the_nodes(self):

        for i in range(self.number_of_nodes):
            urllib.request.urlopen(f"http://localhost:8000/node/connect/0.0.0.0/800{i+1}")
        
        if self.number_of_security_circle == 1:
            for i in range(self.number_of_nodes):
                for i_n in range(self.number_of_nodes):
                    if not i == i_n:
                        urllib.request.urlopen(f"http://localhost:80{i+1}0/node/connect/localhost/800{i_n+1}")
                        time.sleep(1)
        else:
            nodes_list = list(range(self.number_of_nodes))
            circle_list = [nodes_list[x:x+((self.number_of_nodes+1)//self.number_of_security_circle)] for x in range(0, len(nodes_list), ((self.number_of_nodes+1)//self.number_of_security_circle))]

            for circle in circle_list:
                for i in circle:                  
                    for i_n in circle:
                        if not i == i_n:
                            urllib.request.urlopen(f"http://localhost:80{i+1}0/node/connect/localhost/800{i_n+1}")
                            time.sleep(1)                       

    def creating_the_block(self):

        urllib.request.urlopen("http://localhost:8000/settings/test/on")
        urllib.request.urlopen("http://localhost:8000/settings/debug/on")
        for i in range(self.number_of_nodes):
            urllib.request.urlopen(f"http://localhost:80{i+1}0/settings/debug/on")
        urllib.request.urlopen("http://localhost:8000/block/get")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="This is an open source decentralized application network. In this network, you can develop and publish decentralized applications.")


    parser.add_argument('-nn', '--nodenumber', type=int,
                        help='Change Wallet')

    parser.add_argument('-scn', '--securitycirclenumber', type=int,
                        help='Security Circle Number')

    parser.add_argument('-i', '--install', action='store_true',
                        help='Install')   
    
    parser.add_argument('-d', '--delete', action='store_true',
                        help='delete') 

    parser.add_argument('-r', '--run', action='store_true',
                        help='run')  

    parser.add_argument('-s', '--start', action='store_true',
                        help='start')                          
    
    args = parser.parse_args()


    if len(sys.argv) < 2:
        parser.print_help()

    if args.securitycirclenumber is not None:
        temp_environment = Decentra_Network_Local(args.nodenumber, args.securitycirclenumber)
    else:
        temp_environment = Decentra_Network_Local(args.nodenumber)


    if args.delete:
        temp_environment.delete()

    if args.install:
        temp_environment.install()

    if args.run:
        temp_environment.run()

    if args.start:
        temp_environment.start()