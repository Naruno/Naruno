#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import time
from getpass import getpass

from decentra_network.accounts.get_balance import GetBalance
from decentra_network.blockchain.block.create_block import CreateBlock
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.config import MY_TRANSACTION_EXPORT_PATH
from decentra_network.consensus.consensus_main import consensus_trigger
from decentra_network.lib.export import export_the_transactions
from decentra_network.lib.log import get_logger
from decentra_network.lib.mix.mixlib import (banner_maker, menu_maker,
                                             menu_space, question_maker,
                                             quit_menu_maker)
from decentra_network.lib.perpetualtimer import perpetualTimer
from decentra_network.lib.safety import safety_check
from decentra_network.lib.settings_system import (d_mode_settings,
                                                  t_mode_settings,
                                                  the_settings)
from decentra_network.lib.status import Status
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.my_transactions.check_proof import \
    CheckProof
from decentra_network.transactions.my_transactions.get_proof import GetProof
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.print_transactions import PrintTransactions
from decentra_network.transactions.send import send
from decentra_network.wallet.delete_current_wallet import delete_current_wallet
from decentra_network.wallet.ellipticcurve.wallet_create import wallet_create
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import
from decentra_network.wallet.print_wallets import print_wallets
from decentra_network.wallet.wallet_selector import wallet_selector

logger = get_logger("CLI")


def show_menu():
    """
    Prints some information and the menu.
    """

    print(
        banner_maker(
            sc_name="Decentra Network",
            description=
            "This is an open source decentralized application network. In this network, you can develop and publish decentralized applications.",
            author="Decentra Network Developers",
        ))

    print(menu_space() +
          menu_maker(menu_number="pw", menu_text="Print Wallets") +
          menu_maker(menu_number="w", menu_text="Change Wallet") +
          menu_maker(menu_number="cw", menu_text="Create Wallet") +
          menu_maker(menu_number="dw", menu_text="Delete Wallet") +
          menu_space() + menu_maker(menu_number="sc", menu_text="Send Coin") +
          menu_maker(menu_number="scd", menu_text="Send Coin Data") +
          menu_space() +
          menu_maker(menu_number="gb", menu_text="Get Balance") +
          menu_space() +
          menu_maker(menu_number="ndstart", menu_text="Node Start") +
          menu_maker(menu_number="ndstop", menu_text="Node Stop") +
          menu_maker(menu_number="ndconnect", menu_text="Node Connect") +
          menu_maker(menu_number="ndconnectmixdb",
                     menu_text="Node Connect from mixdb") +
          menu_maker(menu_number="ndnewunl", menu_text="Add new UNL node") +
          menu_maker(menu_number="ndid", menu_text="Print my id") +
          menu_space() +
          menu_maker(menu_number="testmodeon", menu_text="Test mode ON") +
          menu_maker(menu_number="testmodeoff", menu_text="Test mode OF") +
          menu_maker(menu_number="debugmodeon", menu_text="Debug mode ON") +
          menu_maker(menu_number="debugmodeoff", menu_text="Debug mode OF") +
          menu_space() + menu_maker(menu_number="exptrcsv",
                                    menu_text="Export Transaction as CSV") +
          menu_maker(menu_number="returntrs",
                     menu_text="Export Transaction as CSV") + menu_space() +
          menu_maker(menu_number="status", menu_text="Prints the status") +
          menu_space() + menu_maker(menu_number="getblock",
                                    menu_text="Get block From Other Nodes") +
          menu_space() +
          menu_maker(menu_number="getproof", menu_text="Get Proof") +
          menu_maker(menu_number="checkproof", menu_text="Check Proof") +
          menu_space())

    print(quit_menu_maker(mode="main"))


def menu():
    """
    The main structure of the cli mode, this function prints the menu,
    listens to the entries, makes the directions.
    """

    animation = [
        "[■□□□□□□□□□]",
        "[■■□□□□□□□□]",
        "[■■■□□□□□□□]",
        "[■■■■□□□□□□]",
        "[■■■■■□□□□□]",
        "[■■■■■■□□□□]",
        "[■■■■■■■□□□]",
        "[■■■■■■■■□□]",
        "[■■■■■■■■■□]",
        "[■■■■■■■■■■]",
    ]

    for item in animation:
        time.sleep(0.1)
        sys.stdout.write("\r" + item)
        sys.stdout.flush()

    while True:
        show_menu()
        choices_input = question_maker(mode="main")

        if choices_input == "pw":
            print_wallets()

        if choices_input == "w":
            wallet_selector(input("Please select wallet: "))

        if choices_input == "cw":
            wallet_create(getpass("Password: "))

        if choices_input == "dw" and input("Are you sure ? (y or n): ") == "y":
            delete_current_wallet()
        if choices_input == "sc":
            block = GetBlock()
            send_tx = send(
                getpass("Password: "),
                input("Please write receiver adress: "),
                amount=input("Coin Amount (ex. 1.0): "),
                block=block,
            )
            if send_tx != False:
                SavetoMyTransaction(send_tx, sended=True)
                server.send_transaction(send_tx)
                SaveBlock(block)
        if choices_input == "scd":
            block = GetBlock()
            send_tx = send(
                getpass("Password: "),
                input("Please write receiver adress: "),
                amount=input("Coin Amount (ex. 1.0): "),
                data=input("Data: "),
                block=block,
            )
            if send_tx != False:
                SavetoMyTransaction(send_tx, sended=True)
                server.send_transaction(send_tx)
                SaveBlock(block)
        if choices_input == "gb":
            GetBalance(GetBlock(), wallet_import(-1, 0))
        if choices_input == "help":
            show_menu()
        if choices_input == "ndstart":
            server(str(input("ip: ")), int(input("port: ")))
        if choices_input == "ndstop":
            server.Server.stop()
        if choices_input == "ndconnect":
            server.Server.connect(str(input("node ip: ")),
                                  int(input("node port: ")))

        if choices_input == "ndconnectmixdb":
            server.connectionfrommixdb()
        if choices_input == "ndnewunl":
            Unl.save_new_unl_node(input("Please write ID of the node: "))
        if choices_input == "ndid":
            print(server.id)
        if choices_input == "testmodeon":
            t_mode_settings(True)
        if choices_input == "testmodeoff":
            t_mode_settings(False)
        if choices_input == "debugmodeon":
            d_mode_settings(True)
        if choices_input == "debugmodeoff":
            d_mode_settings(False)

        if choices_input == "exptrcsv":
            if export_the_transactions():
                print(
                    f"CSV file created in {MY_TRANSACTION_EXPORT_PATH} directory"
                )
            else:
                print("You have not a transaction")

        if choices_input == "returntrs":
            PrintTransactions()

        if choices_input == "getblock":
            if the_settings()["test_mode"]:
                the_block = CreateBlock()
                SaveBlock(the_block)
                server.Server.send_block_to_other_nodes()
                logger.info("Consensus timer is started")
                perpetualTimer(the_block.consensus_timer, consensus_trigger)
            else:
                server.Server.send_me_full_block()

        if choices_input == "status":
            print(Status())

        if choices_input == "getproof":
            print(GetProof(input("Please write the transaction signature: ")))
        if choices_input == "checkproof":
            print(CheckProof(input("Please write the path of proof: ")))

        if choices_input == "0":
            exit()


def arguments():
    """
    This function parses the arguments and makes the directions.
    """

    parser = argparse.ArgumentParser(
        description=
        "This is an open source decentralized application network. In this network, you can develop and publish decentralized applications. Use the menu (-m) or GUI to gain full control and use the node, operation, etc."
    )

    parser.add_argument("-pw",
                        "--printwallet",
                        action="store_true",
                        help="Print Wallets")

    parser.add_argument("-w", "--wallet", type=int, help="Change Wallet")

    parser.add_argument("-cw", "--createwallet", help="Create wallet")

    parser.add_argument("-dw",
                        "--deletewallet",
                        action="store_true",
                        help="Delete wallet")

    parser.add_argument("-gb",
                        "--getbalance",
                        action="store_true",
                        help="Get Balance")

    parser.add_argument("-ndnunl",
                        "--ndnewunl",
                        type=str,
                        help="Add new UNL node")

    parser.add_argument("-ndid",
                        "--ndid",
                        action="store_true",
                        help="Print my id")

    parser.add_argument("-tmon",
                        "--testmodeon",
                        action="store_true",
                        help="Test Mode On")
    parser.add_argument("-tmoff",
                        "--testmodeoff",
                        action="store_true",
                        help="Test Mode Off")

    parser.add_argument("-dmon",
                        "--debugmodeon",
                        action="store_true",
                        help="Debug Mode On")
    parser.add_argument("-dmoff",
                        "--debugmodeoff",
                        action="store_true",
                        help="Debug Mode Off")

    parser.add_argument(
        "-exptrcsv",
        "--exporttransactioncsv",
        action="store_true",
        help="Exports the transaction as csv",
    )

    parser.add_argument(
        "-returntrans",
        "--returntransactions",
        action="store_true",
        help="Exports the transaction as csv",
    )

    parser.add_argument("-st",
                        "--status",
                        action="store_true",
                        help="Exports the transaction as csv")

    parser.add_argument("-gp",
                        "--getproof",
                        type=str,
                        help="Get proof of given transaction signature")

    parser.add_argument("-cp",
                        "--checkproof",
                        type=str,
                        help="Checks the given proof")

    parser.add_argument(
        "-m",
        "--menu",
        action="store_true",
        help="An optional boolean for open the menu.",
    )

    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        help="Interface",
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        help="Timeout",
    )

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()

    if args.printwallet:
        print_wallets()

    if args.getbalance:
        GetBalance(GetBlock(), wallet_import(-1, 0))

    if args.ndid:
        print(server.id)

    if args.testmodeon:
        t_mode_settings(True)
    if args.testmodeoff:
        t_mode_settings(False)
    if args.debugmodeon:
        d_mode_settings(True)
    if args.debugmodeoff:
        d_mode_settings(False)

    if args.exporttransactioncsv:
        if export_the_transactions():
            print(
                f"CSV file created in {MY_TRANSACTION_EXPORT_PATH} directory")
        else:
            print("You have not a transaction")

    if args.returntransactions:
        PrintTransactions()

    if args.status:
        print(Status())

    safety_check(args.interface, args.timeout)

    if args.ndnewunl is not None:
        Unl.save_new_unl_node(args.ndnewunl)

    if args.createwallet is not None:
        wallet_create(args.createwallet)

    if args.deletewallet:
        delete_current_wallet()

    if args.wallet is not None:
        wallet_selector(args.wallet)

    if args.getproof is not None:
        print(GetProof(args.getproof))

    if args.checkproof is not None:
        print(CheckProof(args.checkproof))

    if args.menu:
        menu()


def start():
    """
    Start the CLI mode with arguments.
    """

    logger.info("Starting CLI mode")

    arguments()


if __name__ == "__main__":
    start()
