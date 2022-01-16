#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import time
import sys
import argparse
from getpass import getpass

from config import MY_TRANSACTION_EXPORT_PATH

from transactions.send_the_coin import send_the_coin
from transactions.print_transactions import PrintTransactions

from node.node_connection import ndstart, ndstop, ndconnect, ndconnectmixdb, ndid
from node.unl import save_new_unl_node

from blockchain.block.get_block import GetBlockFromOtherNode
from blockchain.block.create_block import CreateBlock

from lib.mixlib import banner_maker, menu_space, menu_maker, quit_menu_maker, question_maker
from lib.settings_system import the_settings, test_mode, debug_mode
from lib.export import export_the_transactions
from lib.status import Status

from wallet.create_a_wallet import create_a_wallet
from wallet.print_wallets import print_wallets
from wallet.wallet_selector import wallet_selector
from wallet.delete_current_wallet import delete_current_wallet
from wallet.print_balance import print_balance



def show_menu():
    """
    Prints some information and the menu.
    """

    print(banner_maker(sc_name="Decentra Network", description="This is an open source decentralized application network. In this network, you can develop and publish decentralized applications.", author="Decentra Network Developers"))


    print(menu_space() + \
       menu_maker(menu_number="pw", menu_text="Print Wallets")+ \
       menu_maker(menu_number="w", menu_text="Change Wallet")+ \
	   menu_maker(menu_number="cw", menu_text="Create Wallet")+ \
       menu_maker(menu_number="dw", menu_text="Delete Wallet")+ \
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
       menu_maker(menu_number="exptrcsv", menu_text="Export Transaction as CSV")+ \
       menu_maker(menu_number="returntrs", menu_text="Export Transaction as CSV")+ \
       menu_space() + \
       menu_maker(menu_number="status", menu_text="Prints the status")+ \
       menu_space() + \
       menu_maker(menu_number="getblock", menu_text="Get block From Other Nodes")+ \
       menu_space())


    print(quit_menu_maker(mode="main"))


def menu():
    """
    The main structure of the cli mode, this function prints the menu, 
    listens to the entries, makes the directions.
    """

    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

    for i in range(len(animation)):
        time.sleep(0.1)
        sys.stdout.write("\r" + animation[i])
        sys.stdout.flush()    

    while True:
        show_menu()
        choices_input = question_maker(mode="main")

        if choices_input == "pw":
            print_wallets()

        if choices_input == "w":
            wallet_selector()

        if choices_input == "cw":
            create_a_wallet()

        if choices_input == "dw":
            if "y" == input("Are you sure ? (y or n): "):
                delete_current_wallet()
        if choices_input == "sc":
            send_the_coin(input("Please write receiver adress: "), input("Coin Amount (ex. 1.0): "), getpass("Password: "))

        if choices_input == "gb":
            print_balance()
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

        if choices_input == "exptrcsv":
            if export_the_transactions():
                print(f"CSV file created in {MY_TRANSACTION_EXPORT_PATH} directory")
            else:
                print("You have not a transaction")

        if choices_input == "returntrs":
            PrintTransactions()

        if choices_input == "getblock":
            if the_settings()["test_mode"]:
                CreateBlock()
            else:
                GetBlockFromOtherNode()

        if choices_input == "status":
            print(Status())

        if choices_input == "0":
            exit()


def arguments():
    """
    This function parses the arguments and makes the directions.
    """

    parser = argparse.ArgumentParser(description="This is an open source decentralized application network. In this network, you can develop and publish decentralized applications. Use the menu (-m) or GUI to gain full control and use the node, operation, etc.")

    parser.add_argument('-pw', '--printwallet', action='store_true',
                        help='Print Wallets')

    parser.add_argument('-w', '--wallet', type=int,
                        help='Change Wallet')

    parser.add_argument('-cw', '--createwallet',
                        help='Create wallet')

    parser.add_argument('-dw', '--deletewallet', action='store_true',
                        help='Delete wallet')

    parser.add_argument('-gb', '--getbalance', action='store_true',
                        help='Get Balance')

    parser.add_argument('-ndnunl', '--ndnewunl', type=str,
                        help='Add new UNL node')

    parser.add_argument('-ndid', '--ndid', action='store_true',
                        help='Print my id')

    parser.add_argument('-tmon', '--testmodeon', action='store_true',
                        help='Test Mode On')
    parser.add_argument('-tmoff', '--testmodeoff', action='store_true',
                        help='Test Mode Off')

    parser.add_argument('-dmon', '--debugmodeon', action='store_true',
                        help='Debug Mode On')
    parser.add_argument('-dmoff', '--debugmodeoff', action='store_true',
                        help='Debug Mode Off')

    parser.add_argument('-exptrcsv', '--exporttransactioncsv', action='store_true',
                        help='Exports the transaction as csv')                

    parser.add_argument('-returntrans', '--returntransactions', action='store_true',
                        help='Exports the transaction as csv')   

    parser.add_argument('-st', '--status', action='store_true',
                        help='Exports the transaction as csv')

    parser.add_argument('-m', '--menu', action='store_true',
                        help='An optional boolean for open the menu.') 
    
    args = parser.parse_args()


    if len(sys.argv) < 2:
        parser.print_help()

    if args.printwallet:
        print_wallets()

    if not args.wallet is None:
        wallet_selector(args.wallet)

    if not args.createwallet is None:
        create_a_wallet(args.createwallet)

    if args.deletewallet:
        delete_current_wallet()

    if args.getbalance:
        print_balance()

    if not args.ndnewunl is None:
        save_new_unl_node(args.ndnewunl)

    if args.ndid:
        print(ndid())

    if args.testmodeon:
        test_mode(True)
    if args.testmodeoff:
        test_mode(False)
    if args.debugmodeon:
        debug_mode(True)
    if args.debugmodeoff:
        debug_mode(False)

    if args.exporttransactioncsv:
        if export_the_transactions():
            print(f"CSV file created in {MY_TRANSACTION_EXPORT_PATH} directory")
        else:
            print("You have not a transaction")

    if args.returntransactions:
        PrintTransactions()

    if args.status:
        print(Status())

    if args.menu:
        menu()


def start():
    """
    Start the CLI mode with arguments.
    """

    arguments()

if __name__ == '__main__':
    start()
