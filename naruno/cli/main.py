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

from naruno.accounts.get_balance import GetBalance
from naruno.blockchain.block.create_block import CreateBlock
from naruno.blockchain.block.get_block import GetBlock
from naruno.blockchain.block.save_block import SaveBlock
from naruno.config import MY_TRANSACTION_EXPORT_PATH
from naruno.consensus.consensus_main import consensus_trigger
from naruno.lib.backup.naruno_export import naruno_export
from naruno.lib.backup.naruno_import import naruno_import
from naruno.lib.export import export_the_transactions
from naruno.lib.log import get_logger
from naruno.lib.mix.mixlib import (banner_maker, menu_maker, menu_space,
                                   question_maker, quit_menu_maker)
from naruno.lib.perpetualtimer import perpetualTimer
from naruno.lib.safety import safety_check
from naruno.lib.settings_system import (baklava_settings, d_mode_settings,
                                        publisher_mode_settings,
                                        t_mode_settings, the_settings)
from naruno.lib.sign import sign
from naruno.lib.status import Status
from naruno.lib.verify import verify
from naruno.node.server.server import server
from naruno.node.unl import Unl
from naruno.transactions.my_transactions.check_proof import CheckProof
from naruno.transactions.my_transactions.get_proof import GetProof
from naruno.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from naruno.transactions.print_transactions import PrintTransactions
from naruno.transactions.send import send
from naruno.wallet.delete_current_wallet import delete_current_wallet
from naruno.wallet.print_wallets import print_wallets
from naruno.wallet.wallet_create import wallet_create
from naruno.wallet.wallet_import import wallet_import
from naruno.wallet.wallet_selector import wallet_selector

logger = get_logger("CLI")


def show_menu():
    """
    Prints some information and the menu.
    """

    print(
        banner_maker(
            sc_name="Naruno",
            description=
            "Naruno is a lightning-fast, secure, and scalable blockchain that is able to create transaction proofs and verification via raw data and timestamp. We remove the archive nodes and lazy web3 integrations. With Naruno everyone can get the proof (5-10MB) of their transactions via their nodes and after everyone can use in another node for verification the raw data and timestamp. Also you can integrate your web3 applications with 4 code lines (just python for now) via our remote app system.",
            author="Naruno Developers",
        ))

    print(
        menu_space() +
        menu_maker(menu_number="pw", menu_text="Print Wallets") +
        menu_maker(menu_number="w", menu_text="Change Wallet") +
        menu_maker(menu_number="cw", menu_text="Create Wallet") +
        menu_maker(menu_number="dw", menu_text="Delete Wallet") +
        menu_space() + menu_maker(menu_number="sc", menu_text="Send Coin") +
        menu_maker(menu_number="scd", menu_text="Send Coin Data") +
        menu_space() + menu_maker(menu_number="gb", menu_text="Get Balance") +
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
        menu_space() +
        menu_maker(menu_number="narunoexport", menu_text="Export backup") +
        menu_maker(menu_number="narunoimport", menu_text="Import backup") +
        menu_space() +
        menu_maker(menu_number="sign", menu_text="Sign and export an data") +
        menu_maker(menu_number="verify", menu_text="Verify the signed data") +
        menu_space() + menu_maker(menu_number="publishermodeon",
                                  menu_text="Publisher Mode On") +
        menu_maker(menu_number="publishermodeoff",
                   menu_text="Publisher Mode Off") + menu_space())

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
            print(GetBalance(wallet_import(-1, 0)))
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

        if choices_input == "publishermodeon":
            publisher_mode_settings(True)
        if choices_input == "publishermodeoff":
            publisher_mode_settings(False)

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

        if choices_input == "narunoexport":
            print(naruno_export())
        if choices_input == "narunoimport":
            print(
                naruno_import(
                    input("Please write the path of exported backup: ")))

        if choices_input == "sign":
            print(sign(input("Please write the data: "),
                       getpass("Password: ")))

        if choices_input == "verify":
            print(verify(input("Please write the signed data path: ")))

        input("Press enter to continue (screen will be cleaned)...")
        os.system("cls" if os.name == "nt" else "clear")

        if choices_input == "0":
            exit()


def arguments():
    """
    This function parses the arguments and makes the directions.
    """

    parser = argparse.ArgumentParser(
        description=
        "Naruno is a lightning-fast, secure, and scalable blockchain that is able to create transaction proofs and verification via raw data and timestamp. We remove the archive nodes and lazy web3 integrations. With Naruno everyone can get the proof (5-10MB) of their transactions via their nodes and after everyone can use in another node for verification the raw data and timestamp. Also you can integrate your web3 applications with 4 code lines (just python for now) via our remote app system. Use the menu (-m) or GUI to gain full control and use the node, operation, etc."
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

    parser.add_argument("-pmon",
                        "--publishermodeon",
                        action="store_true",
                        help="Publisher Mode On")
    parser.add_argument("-pmoff",
                        "--publishermodeoff",
                        action="store_true",
                        help="Publisher Mode Off")

    parser.add_argument("-bon",
                        "--baklavaon",
                        action="store_true",
                        help="Baklava On")
    parser.add_argument("-boff",
                        "--baklavaoff",
                        action="store_true",
                        help="Baklava Off")

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

    parser.add_argument("-narunoexport",
                        "--narunoexport",
                        action="store_true",
                        help="Export backup")

    parser.add_argument("-narunoimport",
                        "--narunoimport",
                        type=str,
                        help="Import backup")

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
        print(GetBalance(wallet_import(-1, 0)))

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

    if args.publishermodeon:
        publisher_mode_settings(True)
    if args.publishermodeoff:
        publisher_mode_settings(False)

    if args.baklavaon:
        baklava_settings(True)
    if args.baklavaoff:
        baklava_settings(False)

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

    if args.narunoexport:
        print(naruno_export())

    if args.narunoimport is not None:
        naruno_import(args.narunoimport)

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
