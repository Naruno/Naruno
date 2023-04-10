#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import argparse
import json
import os
import random
import signal
import sys
import time
import urllib

import requests


class Naruno_Local:
    def __init__(self, number_of_nodes=3, number_of_security_circle=1):
        self.number_of_nodes = number_of_nodes - 1
        self.number_of_security_circle = number_of_security_circle
        nodes_list = list(range(self.number_of_nodes))
        self.circles = [
            nodes_list[
                x : x + ((self.number_of_nodes + 1) // self.number_of_security_circle)
            ]
            for x in range(
                0,
                len(nodes_list),
                ((self.number_of_nodes + 1) // self.number_of_security_circle),
            )
        ]

        normal_length = len(self.circles[0])

        for circle in self.circles:
            leader = random.choice(circle)
            while leader == 0 and circle.index(leader) + 1 > normal_length:
                leader = random.choice(circle)

            for circle_ in self.circles:
                if circle_ != circle:
                    circle_.append(leader)

        self.circles = [list(dict.fromkeys(circle)) for circle in self.circles]

    def start(self):
        time.sleep(1 * self.number_of_nodes)
        self.debug_and_test_mode()
        self.creating_the_wallets()
        self.starting_the_nodest()
        self.unl_nodes_settting()
        self.connecting_the_nodes()
        self.creating_the_block()
        time.sleep(22)

    def install(self):
        time.sleep(1 * self.number_of_nodes)
        os.system("pip3 install -r Naruno/requirements/api.txt")
        os.system("cp -r -f Naruno Naruno-0")
        for i in range(self.number_of_nodes):
            os.system(f"cp -r -f Naruno Naruno-{i+1}")

    def delete(self):
        time.sleep(1 * self.number_of_nodes)
        os.system("rm -r -f Naruno-*")

        for line in os.popen("ps ax | grep python3 | grep -v grep"):
            fields = line.split()
            if "/naruno/api/main.py" in fields[5]:
                os.kill(int(fields[0]), signal.SIGKILL)
        os.system("rm -r -f Naruno-0.out")
        for i in range(self.number_of_nodes):
            os.system(f"rm -r -f Naruno-{i + 1}.out")

    def run(self):
        time.sleep(1 * self.number_of_nodes)
        os.system("nohup python3 Naruno-0/naruno/api/main.py >> Naruno-0.out &")
        for i in range(self.number_of_nodes):
            os.system(
                f"nohup python3 Naruno-{i+1}/naruno/api/main.py -p {8100 + i + 1} >> Naruno-{i + 1}.out &"
            )

    def debug_and_test_mode(self):
        time.sleep(1 * self.number_of_nodes)
        urllib.request.urlopen("http://localhost:8000/settings/test/on")
        urllib.request.urlopen("/settings/functionaltest/on")
        urllib.request.urlopen("http://localhost:8000/settings/debug/on")
        for i in range(self.number_of_nodes):
            urllib.request.urlopen(f"http://localhost:{8100 + i + 1}/settings/debug/on")

    def creating_the_wallets(self):
        time.sleep(1 * self.number_of_nodes)
        urllib.request.urlopen("http://localhost:8000/wallet/create/123")
        for i in range(self.number_of_nodes):
            urllib.request.urlopen(f"http://localhost:{8100 + i + 1}/wallet/create/123")

    def starting_the_nodest(self):
        time.sleep(1 * self.number_of_nodes)
        urllib.request.urlopen("http://localhost:8000/node/start/0.0.0.0/7999")
        for i in range(self.number_of_nodes):
            urllib.request.urlopen(
                f"http://localhost:{8100 + i + 1}/node/start/0.0.0.0/{8010 + i + 1}"
            )

    def unl_nodes_settting(self):
        time.sleep(1 * self.number_of_nodes)
        node_id_1 = json.loads(
            urllib.request.urlopen("http://localhost:8000/node/id").read().decode()
        )
        for i in range(self.number_of_nodes):
            urllib.request.urlopen(
                f"http://localhost:{8100 + i + 1}/node/newunl/?{node_id_1}"
            )

        if self.number_of_security_circle == 1:
            for i in range(self.number_of_nodes):
                node_id_2 = json.loads(
                    urllib.request.urlopen(f"http://localhost:{8100 + i + 1}/node/id")
                    .read()
                    .decode()
                )
                urllib.request.urlopen(
                    f"http://localhost:8000/node/newunl/?{node_id_2}"
                )
                for i_n in range(self.number_of_nodes):
                    if i != i_n:
                        urllib.request.urlopen(
                            f"http://localhost:{8100 + i_n + 1}/node/newunl/?{node_id_2}"
                        )
        else:
            for circle in self.circles:
                for i in circle:
                    node_id_2 = json.loads(
                        urllib.request.urlopen(
                            f"http://localhost:{8100 + i + 1}/node/id"
                        )
                        .read()
                        .decode()
                    )
                    urllib.request.urlopen(
                        f"http://localhost:8000/node/newunl/?{node_id_2}"
                    )
                    for i_n in circle:
                        if i != i_n:
                            urllib.request.urlopen(
                                f"http://localhost:{8100 + i_n + 1}/node/newunl/?{node_id_2}"
                            )

    def connecting_the_nodes(self):
        time.sleep(1 * self.number_of_nodes)
        for i in range(self.number_of_nodes):
            urllib.request.urlopen(
                f"http://localhost:8000/node/connect/0.0.0.0/{8010 + i + 1}"
            )
        time.sleep(1 * self.number_of_nodes)
        if self.number_of_security_circle == 1:
            for i in range(self.number_of_nodes):
                for i_n in range(self.number_of_nodes):
                    if i != i_n:
                        urllib.request.urlopen(
                            f"http://localhost:{8100 + i + 1}/node/connect/0.0.0.0/{8010 + i_n + 1}"
                        )
                time.sleep(1 * self.number_of_nodes)

        else:
            for circle in self.circles:
                for i in circle:
                    for i_n in circle:
                        if i != i_n:
                            urllib.request.urlopen(
                                f"http://localhost:{8100 + i + 1}/node/connect/0.0.0.0/{8010 + i_n + 1}"
                            )
                    time.sleep(1 * self.number_of_nodes)

    def creating_the_block(self):
        time.sleep(1 * self.number_of_nodes)
        urllib.request.urlopen("http://localhost:8000/block/get")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Naruno is a lightning-fast, secure, and scalable blockchain that is able to create transaction proofs and verification via raw data and timestamp. We remove the archive nodes and lazy web3 integrations. With Naruno everyone can get the proof (5-10MB) of their transactions via their nodes and after everyone can use in another node for verification the raw data and timestamp. Also you can integrate your web3 applications with 4 code lines (just python for now) via our remote app system."
    )

    parser.add_argument("-nn", "--nodenumber", type=int, help="Node Number")

    parser.add_argument(
        "-scn", "--securitycirclenumber", type=int, help="Security Circle Number"
    )

    parser.add_argument("-i", "--install", action="store_true", help="Install")

    parser.add_argument("-d", "--delete", action="store_true", help="delete")

    parser.add_argument("-r", "--run", action="store_true", help="run")

    parser.add_argument("-s", "--start", action="store_true", help="start")

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()

    if args.securitycirclenumber is not None:
        temp_environment = Naruno_Local(args.nodenumber, args.securitycirclenumber)
    else:
        temp_environment = Naruno_Local(args.nodenumber)

    if args.delete:
        temp_environment.delete()

    if args.install:
        temp_environment.install()

    if args.run:
        temp_environment.run()

    if args.start:
        temp_environment.start()
