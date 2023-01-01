#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import argparse
import os
import sys

from flask import Flask
from flask import jsonify
from flask import request
from waitress import serve
from waitress.server import create_server

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from flask_cors import CORS

from decentra_network.accounts.get_balance import GetBalance
from decentra_network.blockchain.block.create_block import CreateBlock
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.consensus.consensus_main import consensus_trigger
from decentra_network.lib.export import export_the_transactions
from decentra_network.lib.log import get_logger
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
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from decentra_network.transactions.my_transactions.get_proof import GetProof
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.send import send
from decentra_network.wallet.delete_current_wallet import delete_current_wallet
from decentra_network.wallet.ellipticcurve.wallet_create import wallet_create
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import
from decentra_network.wallet.print_wallets import print_wallets
from decentra_network.wallet.wallet_selector import wallet_selector

logger = get_logger("API")

app = Flask(__name__)
CORS(app,
     resources={
         r"/export/block/*": {
             "origins": "*"
         },
         r"/status": {
             "origins": "*"
         }
     })

custom_block = None
custom_current_time = None
custom_sequence_number = None
custom_balance = None
custom_server = None

custom_TEMP_BLOCK_PATH = None
custom_TEMP_ACCOUNTS_PATH = None
custom_TEMP_BLOCKSHASH_PATH = None
custom_TEMP_BLOCKSHASH_PART_PATH = None

account_list = None

custom_wallet = None

custom_CONNECTED_NODES_PATH = None

custom_consensus_trigger = None
custom_consensus_trigger_result = None

custom_transactions = None
custom_MY_TRANSACTION_EXPORT_PATH = None

custom_UNL_NODES_PATH = None
custom_first_block = None
custom_new_block = None
custom_connections = None

custom_account_list = None


@app.route("/wallet/print", methods=["GET"])
def print_wallets_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(print_wallets())


@app.route("/wallet/change/<number>", methods=["GET"])
def wallet_change_page(number):
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    wallet_selector(number)
    return jsonify(print_wallets())


@app.route("/wallet/create/<password>", methods=["GET"])
def create_wallet_page(password):
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    wallet_create(password)
    return jsonify(print_wallets())


@app.route("/wallet/delete", methods=["GET"])
def delete_wallets_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    delete_current_wallet()
    return jsonify(print_wallets())


@app.route("/send/", methods=["POST"])
def send_coin_data_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.form}")
    address = str(
        request.form["to_user"]) if "to_user" in request.form else None
    amount = float(
        request.form["amount"]) if "amount" in request.form else None
    data = str(request.form["data"]) if "data" in request.form else ""
    password = str(
        request.form["password"]) if "password" in request.form else None
    block = (GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
             if custom_block is None else custom_block)
    send_tx = send(
        password,
        address,
        amount=amount,
        data=data,
        block=block,
        custom_current_time=custom_current_time,
        custom_sequence_number=custom_sequence_number,
        custom_balance=custom_balance,
        custom_account_list=custom_account_list,
    )
    if send_tx != False:
        SavetoMyTransaction(send_tx, sended=True)
        server.send_transaction(
            send_tx,
            custom_current_time=custom_current_time,
            custom_sequence_number=custom_sequence_number,
            custom_balance=custom_balance,
            custom_server=custom_server,
        )
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
    result = send_tx.dump_json() if send_tx != False else False
    return jsonify(result)


@app.route("/wallet/balance", methods=["GET"])
def balance_wallets_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    the_wallet = wallet_import(-1,
                               0) if custom_wallet is None else custom_wallet
    the_block = (GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
                 if custom_block is None else custom_block)
    return jsonify(
        GetBalance(the_wallet, account_list=account_list, block=the_block))


@app.route("/node/start/<ip>/<port>", methods=["GET"])
def node_start_page(ip, port):
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    server(str(ip), int(port))
    return jsonify("OK")


@app.route("/node/stop", methods=["GET"])
def node_stop_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    server.Server.stop()
    return jsonify("OK")


@app.route("/node/connect/<ip>/<port>", methods=["GET"])
def node_connect_page(ip, port):
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    server.Server.connect(str(ip), int(port))
    return jsonify("OK")


@app.route("/node/connectmixdb", methods=["GET"])
def node_connectmixdb_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    server.connectionfrommixdb(
        custom_server=custom_server,
        custom_CONNECTED_NODES_PATH=custom_CONNECTED_NODES_PATH,
    )
    return jsonify("OK")


# /node/newunl/?MFYw......
@app.route("/node/newunl/", methods=["GET"])
def node_newunl_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    Unl.save_new_unl_node(request.query_string.decode("utf-8"))
    return jsonify("OK")


@app.route("/node/id", methods=["GET"])
def node_id_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(server.id)


@app.route("/settings/test/on", methods=["GET"])
def settings_test_on_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    t_mode_settings(True)
    return jsonify("OK")


@app.route("/settings/test/off", methods=["GET"])
def settings_test_off_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    t_mode_settings(False)
    return jsonify("OK")


@app.route("/settings/debug/on", methods=["GET"])
def settings_debug_on_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    app.config["DEBUG"] = True
    d_mode_settings(True)
    return jsonify("OK")


@app.route("/settings/debug/off", methods=["GET"])
def settings_debug_off_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    app.config["DEBUG"] = False
    d_mode_settings(False)
    return jsonify("OK")


@app.route("/block/get", methods=["GET"])
def block_get_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    the_server = server.Server if custom_server is None else custom_server
    if the_settings()["test_mode"]:
        the_block = CreateBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        the_server.send_block_to_other_nodes()
        logger.info("Consensus timer is started")
        the_consensus_trigger = (consensus_trigger
                                 if custom_consensus_trigger is None else
                                 custom_consensus_trigger)
        trigger = perpetualTimer(the_block.consensus_timer,
                                 the_consensus_trigger)
        global custom_consensus_trigger_result
        custom_consensus_trigger_result = trigger
    else:
        the_server.send_me_full_block()
    return jsonify("OK")


@app.route("/export/transactions/csv", methods=["GET"])
def export_transaction_csv_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(
        export_the_transactions(
            custom_transactions=custom_transactions,
            custom_MY_TRANSACTION_EXPORT_PATH=custom_MY_TRANSACTION_EXPORT_PATH,
        ))


@app.route("/transactions/sended/validated", methods=["GET"])
def transaction_sended_validated_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(
        GetMyTransaction(sended=True, validated=True, turn_json=True))


@app.route("/transactions/sended/not_validated", methods=["GET"])
def transaction_sended_not_validated_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(
        GetMyTransaction(sended=True, validated=False, turn_json=True))


@app.route("/transactions/received", methods=["GET"])
def transaction_received_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(GetMyTransaction(sended=False, turn_json=True))


@app.route("/transactions/all", methods=["GET"])
def transaction_all_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(GetMyTransaction(turn_json=True))


@app.route("/status", methods=["GET"])
def status_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(
        Status(
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_UNL_NODES_PATH=custom_UNL_NODES_PATH,
            custom_first_block=custom_first_block,
            custom_new_block=custom_new_block,
            custom_connections=custom_connections,
            custom_transactions=custom_transactions,
        ))


@app.route("/proof/get/", methods=["POST"])
def proof_get_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.form}")
    signature = str(
        request.form["signature"]) if "signature" in request.form else None
    custom_PROOF_PATH = (str(request.form["custom_PROOF_PATH"])
                         if "custom_PROOF_PATH" in request.form else None)
    custom_BLOCKS_PATH = (str(request.form["custom_BLOCKS_PATH"])
                          if "custom_BLOCKS_PATH" in request.form else None)
    custom_TEMP_ACCOUNTS_PATH = (str(request.form["custom_TEMP_ACCOUNTS_PATH"])
                                 if "custom_TEMP_ACCOUNTS_PATH" in request.form
                                 else None)
    custom_TEMP_BLOCKSHASH_PATH = (
        str(request.form["custom_TEMP_BLOCKSHASH_PATH"])
        if "custom_TEMP_BLOCKSHASH_PATH" in request.form else None)
    custom_TEMP_BLOCKSHASH_PART_PATH = (
        str(request.form["custom_TEMP_BLOCKSHASH_PART_PATH"])
        if "custom_TEMP_BLOCKSHASH_PART_PATH" in request.form else None)

    return jsonify(
        GetProof(
            signature,
            custom_PROOF_PATH=custom_PROOF_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        ))


@app.route("/proof/check/", methods=["POST"])
def proof_check_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.form}")
    path = str(request.form["path"]) if "path" in request.form else None
    custom_TEMP_BLOCKSHASH_PART_PATH = (
        str(request.form["custom_TEMP_BLOCKSHASH_PART_PATH"])
        if "custom_TEMP_BLOCKSHASH_PART_PATH" in request.form else None)
    return jsonify(
        CheckProof(
            path,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        ))


@app.route("/export/block/json", methods=["GET"])
def export_block_json_page():
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    the_block = (GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
                 if custom_block is None else custom_block)
    return jsonify(the_block.dump_json())


@app.errorhandler(500)
def handle_exception(e):
    logger.exception(f"500: {e}")
    return jsonify("500"), 500


@app.errorhandler(404)
def page_not_found(e):
    logger.error(f"404: {e}")
    return jsonify("404"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    logger.error(f"405: {e}")
    return jsonify("405"), 405


def start(port=None, test=False):
    """
    Start the API server.
    """

    parser = argparse.ArgumentParser(
        description=
        "This is an open source decentralized application network. In this network, you can develop and publish decentralized applications."
    )

    parser.add_argument("-p",
                        "--port",
                        default=8000,
                        type=int,
                        help="Add new UNL node")

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

    args.port = args.port if port is None else int(port)

    safety_check(args.interface, args.timeout)

    logger.info(f"Starting API on port {args.port}")
    result = (serve(app, host="0.0.0.0", port=args.port) if test is False else
              create_server(app, host="0.0.0.0", port=args.port))
    return result


if __name__ == "__main__":
    start()
