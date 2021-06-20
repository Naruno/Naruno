#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import time
import sys
from getpass import getpass

from hashlib import sha256
from wallet.wallet import Wallet_Create, Wallet_Import, get_saved_wallet, Wallet_Delete

from transactions.send_coin import send_coin
from node.node_connection import ndstart, ndstop, ndconnect, ndconnectmixdb, ndid
from node.unl import save_new_unl_node

from lib.mixlib import banner_maker, menu_space, menu_maker, quit_menu_maker, question_maker

from blockchain.block.get_block import GetBlock, GetBlockFromOtherNode
from blockchain.block.create_block import CreateBlock

from lib.settings_system import the_settings, test_mode, debug_mode, change_wallet

from accounts.get_balance import GetBalance


def show_menu():
    """
    Prints some information and the menu.
    """

    print(banner_maker(sc_name="Decentra Network", description="This is an open source decentralized application network. In this network, you can develop and publish decentralized applications.", author="Decentra Network Developers"))


    print(menu_space() + \
       menu_maker(menu_number="w", menu_text="Wallets")+ \
	   menu_maker(menu_number="cw", menu_text="Create wallet")+ \
       menu_maker(menu_number="dw", menu_text="Delete wallet")+ \
	   menu_space() + \
	   menu_maker(menu_number="sc", menu_text="Send Coin")+ \
       menu_space() + \
       menu_maker(menu_number="gb", menu_text="Get Balance")+ \
       menu_space() + \
       menu_maker(menu_number="ndstart", menu_text="Node Start")+ \
       menu_maker(menu_number="ndstop", menu_text="Node Stop")+ \
       menu_maker(menu_number="ndconnect", menu_text="Node Connect")+ \
       menu_maker(menu_number="ndconnectmixdb", menu_text="Node Connect from mixdb")+ \
       menu_maker(menu_number="ndnewunl", menu_text="Add new UNL node")+ \
       menu_maker(menu_number="ndid", menu_text="Print my id")+ \
       menu_space() + \
       menu_maker(menu_number="testmodeon", menu_text="Test mode ON")+ \
       menu_maker(menu_number="testmodeoff", menu_text="Test mode OF")+ \
       menu_maker(menu_number="debugmodeon", menu_text="Debug mode ON")+ \
       menu_maker(menu_number="debugmodeoff", menu_text="Debug mode OF")+ \
       menu_space() + \
       menu_maker(menu_number="getblock", menu_text="Get block From Other Nodes")+ \
       menu_space())


    print(quit_menu_maker(mode="main"))


def menu():
    """
    The main structure of the cli mode, this function prints the menu, 
    listens to the entries, makes the directions.
    """

    while True:
        show_menu()
        choices_input = question_maker(mode="main")

        if choices_input == "w":
            all_wallets = list(get_saved_wallet())
            if not len(all_wallets) == 0:

                current_wallet = the_settings()["wallet"]
                for wallet in all_wallets:
                    number = all_wallets.index(wallet)
                    address = Wallet_Import(all_wallets.index(wallet),3)
                    if not current_wallet == number:
                        print(menu_maker(menu_number=number, menu_text=address))
                    else:
                        print(menu_maker(menu_number=number, menu_text=address + " - CURRENTLY USED"))

                while True:
                    try:
                        new_wallet = input("Please select wallet: ")
                        if int(new_wallet) in list(range(len(all_wallets))):
                            change_wallet(int(new_wallet))
                            break
                        else:
                            print("There is no such wallet")
                    except:
                        print("This is not a number")
            else:
                print("There is no wallet")

        if choices_input == "cw":
            password = getpass("Password: ")
            Wallet_Create(password)
            del password
        if choices_input == "dw":
            if not the_settings()["wallet"] == 0:
                if "y" == input("Are you sure ? (y or n): "):
                    saved_wallets = get_saved_wallet()
                    selected_wallet_pubkey = Wallet_Import(int(the_settings()["wallet"]),0)
                    for each_wallet in saved_wallets:
                        if selected_wallet_pubkey == saved_wallets[each_wallet]["publickey"]:
                            change_wallet(0)
                            Wallet_Delete(each_wallet)
            else:
                print("First wallet cannot be deleted.")
        if choices_input == "sc":
            temp_coin_amount = input("Coin Amount (ex. 1.0): ")
            type_control = False
            try:
                float(temp_coin_amount)
                type_control = True
            except:
                print("This is not float coin amount.")

            receiver = input("Please write receiver adress: ")

            if type_control and not float(temp_coin_amount) < GetBlock().minumum_transfer_amount:
                password = getpass("Password: ")
                if Wallet_Import(int(the_settings()["wallet"]),2) == sha256(password.encode("utf-8")).hexdigest():
                    print(password)
                    send_coin(float(temp_coin_amount), receiver, password)
                else:
                    print("Password is not correct")
                del password

        if choices_input == "gb":
            print(GetBalance(Wallet_Import(-1,0), GetBlock()))
        if choices_input == "help":
            show_menu()
        if choices_input == "ndstart":
            ndstart(str(input("ip: ")), int(input("port: ")))
        if choices_input == "ndstop":
            ndstop()
        if choices_input == "ndconnect":
            ndconnect(str(input("node ip: ")), int(input("node port: ")))

        if choices_input == "ndconnectmixdb":
            ndconnectmixdb()
        if choices_input == "ndnewunl":
            save_new_unl_node(input("Please write ID of the node: "))
        if choices_input == "ndid":
            print(ndid())
        if choices_input == "testmodeon":
            test_mode(True)
        if choices_input == "testmodeoff":
            test_mode(False)
        if choices_input == "debugmodeon":
            debug_mode(True)
        if choices_input == "debugmodeoff":
            debug_mode(False)


        if choices_input == "getblock":
            if the_settings()["test_mode"]:
                CreateBlock()
            else:
                GetBlockFromOtherNode()



        if choices_input == "0":
            exit()


if __name__ == '__main__':
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

    for i in range(len(animation)):
        time.sleep(0.1)
        sys.stdout.write("\r" + animation[i])
        sys.stdout.flush()
    menu()
