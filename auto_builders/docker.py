#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import urllib.request, json
import time
import os
import argparse
import sys


class Decentra_Network_Docker:

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
        os.system("docker image tag ghcr.io/decentra-network/api decentra-network-api")
        os.system("docker network create --subnet=172.19.0.0/16 dn-net")
        for i in range(self.number_of_nodes):
            os.system(f"docker tag decentra-network-api {i}")

    def delete(self):
        os.system("docker rm -f $(docker ps -a -q -f ancestor=decentra-network-api)")
        os.system("docker volume rm $(docker volume ls -q -f name=decentra-network)")

        os.system("docker network rm dn-net")

    def run(self):

        os.system("docker run -v decentra-network:/Decentra-Network/src/db/ --network dn-net -p 8000:8000 -p 7999:7999 -dit decentra-network-api")
        for i in range(self.number_of_nodes):
            os.system(f"docker run -v decentra-network-{i}:/Decentra-Network/src/db/ --network dn-net -p 8{i+1}00:8000 -p 80{i+1}0:80{i+1}0 -dit {i}")

    def creating_the_wallets(self):

        create_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8000/wallet/create/123").read().decode())
        for i in range(self.number_of_nodes):
            create_wallet_2 = json.loads(urllib.request.urlopen(f"http://localhost:8{i+1}00/wallet/create/123").read().decode())

    def starting_the_nodest(self):

        node_start_1 = json.loads(urllib.request.urlopen("http://localhost:8000/node/start/172.19.0.2/7999").read().decode())
        for i in range(self.number_of_nodes):
            node_start_2 = json.loads(urllib.request.urlopen(f"http://localhost:8{i+1}00/node/start/172.19.0.{i+3}/80{i+1}0").read().decode())

    def unl_nodes_settting(self):

        node_id_1 = json.loads(urllib.request.urlopen("http://localhost:8000/node/id").read().decode())
        for i in range(self.number_of_nodes):
            urllib.request.urlopen(f"http://localhost:8{i+1}00/node/newunl/?{node_id_1}")
        
        if self.number_of_security_circle == 1:
            for i in range(self.number_of_nodes):
                node_id_2 = json.loads(urllib.request.urlopen(f"http://localhost:8{i+1}00/node/id").read().decode())
                urllib.request.urlopen(f"http://localhost:8000/node/newunl/?{node_id_2}")
                for i_n in range(self.number_of_nodes):
                    if not i == i_n:
                        urllib.request.urlopen(f"http://localhost:8{i_n+1}00/node/newunl/?{node_id_2}")
        else:
            nodes_list = list(range(self.number_of_nodes))
            circle_list = [nodes_list[x:x+((self.number_of_nodes+1)//self.number_of_security_circle)] for x in range(0, len(nodes_list), ((self.number_of_nodes+1)//self.number_of_security_circle))]

            for circle in circle_list:
                for i in circle:
                    node_id_2 = json.loads(urllib.request.urlopen(f"http://localhost:8{i+1}00/node/id").read().decode())
                    urllib.request.urlopen(f"http://localhost:8000/node/newunl/?{node_id_2}")                    
                    for i_n in circle:
                        if not i == i_n:
                            urllib.request.urlopen(f"http://localhost:8{i_n+1}00/node/newunl/?{node_id_2}")

    def connecting_the_nodes(self):

        for i in range(self.number_of_nodes):
            urllib.request.urlopen(f"http://localhost:8000/node/connect/172.19.0.{i+3}/80{i+1}0")
        
        if self.number_of_security_circle == 1:
            for i in range(self.number_of_nodes):
                for i_n in range(self.number_of_nodes):
                    if not i == i_n:
                        urllib.request.urlopen(f"http://localhost:8{i+1}00/node/connect/172.19.0.{i_n+3}/80{i_n+1}0")
                        time.sleep(1)
        else:
            nodes_list = list(range(self.number_of_nodes))
            circle_list = [nodes_list[x:x+((self.number_of_nodes+1)//self.number_of_security_circle)] for x in range(0, len(nodes_list), ((self.number_of_nodes+1)//self.number_of_security_circle))]

            for circle in circle_list:
                for i in circle:                  
                    for i_n in circle:
                        if not i == i_n:
                            urllib.request.urlopen(f"http://localhost:8{i+1}00/node/connect/172.19.0.{i_n+3}/80{i_n+1}0")
                            time.sleep(1)            

    def creating_the_block(self):

        urllib.request.urlopen("http://localhost:8000/settings/test/on")
        urllib.request.urlopen("http://localhost:8000/settings/debug/on")
        for i in range(self.number_of_nodes):
            urllib.request.urlopen(f"http://localhost:8{i+1}00/settings/debug/on")
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
        temp_environment = Decentra_Network_Docker(args.nodenumber, args.securitycirclenumber)
    else:
        temp_environment = Decentra_Network_Docker(args.nodenumber)


    if args.delete:
        temp_environment.delete()

    if args.install:
        temp_environment.install()

    if args.run:
        temp_environment.run()

    if args.start:
        temp_environment.start()