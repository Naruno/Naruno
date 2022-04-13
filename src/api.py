#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import argparse
import sys

import flask
from blockchain.block.create_block import CreateBlock
from blockchain.block.get_block import GetBlockFromOtherNode
from flask import jsonify
from flask import request
from lib.export import export_the_transactions
from lib.settings_system import debug_mode
from lib.settings_system import test_mode
from lib.settings_system import the_settings
from lib.status import Status
from node.node import Node
from node.node_connection import Node_Connection
from node.unl import Unl
from transactions.get_my_transaction import GetMyTransaction
from transactions.send import send
from waitress import serve
from wallet.create_a_wallet import create_a_wallet
from wallet.delete_current_wallet import delete_current_wallet
from wallet.print_balance import print_balance
from wallet.print_wallets import print_wallets
from wallet.wallet_selector import wallet_selector

app = flask.Flask(__name__)


@app.route("/wallet/print", methods=["GET"])
def print_wallets_page():
    return jsonify(print_wallets())


@app.route("/wallet/change/<number>", methods=["GET"])
def wallet_change_page(number):
    wallet_selector(number)
    return jsonify(print_wallets())


@app.route("/wallet/create/<password>", methods=["GET"])
def create_wallet_page(password):
    create_a_wallet(password)
    return jsonify(print_wallets())


@app.route("/wallet/delete", methods=["GET"])
def delete_wallets_page():
    delete_current_wallet()
    return jsonify(print_wallets())


@app.route("/send/coin/<address>/<amount>/<password>", methods=["GET"])
def send_coin_page(address, amount, password):
    send(password, address, amount)
    return jsonify("OK")


@app.route("/send/coin-data/<address>/<amount>/<data>/<password>", methods=["GET"])
def send_coin_data_page(address, amount, data, password):
    send(password, address, amount, data)
    return jsonify("OK")


@app.route("/wallet/balance", methods=["GET"])
def balance_wallets_page():
    return jsonify(print_balance())


@app.route("/node/start/<ip>/<port>", methods=["GET"])
def node_start_page(ip, port):
    Node(str(ip), int(port))
    return jsonify("OK")


@app.route("/node/stop", methods=["GET"])
def node_stop_page():
    Node.main_node.stop()
    return jsonify("OK")


@app.route("/node/connect/<ip>/<port>", methods=["GET"])
def node_connect_page(ip, port):
    Node_Connection.connect(str(ip), int(port))
    return jsonify("OK")


@app.route("/node/connectmixdb", methods=["GET"])
def node_connectmixdb_page():
    Node_Connection.connectmixdb()
    return jsonify("OK")


# /node/newunl/?MFYw......
@app.route("/node/newunl/", methods=["GET"])
def node_newunl_page():
    Unl.save_new_unl_node(request.query_string.decode("utf-8"))
    return jsonify("OK")


@app.route("/node/id", methods=["GET"])
def node_id_page():
    return jsonify(Node.id)


@app.route("/settings/test/on", methods=["GET"])
def settings_test_on_page():
    test_mode(True)
    return jsonify("OK")


@app.route("/settings/test/off", methods=["GET"])
def settings_test_off_page():
    test_mode(False)
    return jsonify("OK")


@app.route("/settings/debug/on", methods=["GET"])
def settings_debug_on_page():
    app.config["DEBUG"] = True
    debug_mode(True)
    return jsonify("OK")


@app.route("/settings/debug/off", methods=["GET"])
def settings_debug_off_page():
    app.config["DEBUG"] = False
    debug_mode(False)
    return jsonify("OK")


@app.route("/block/get", methods=["GET"])
def block_get_page():
    if the_settings()["test_mode"]:
        CreateBlock()
    else:
        GetBlockFromOtherNode()
    return jsonify("OK")


@app.route("/export/transactions/csv", methods=["GET"])
def export_transaction_csv_page():
    if export_the_transactions():
        return jsonify("OK")
    else:
        return jsonify("You have not a transaction")


@app.route("/export/transactions/json", methods=["GET"])
def export_transaction_json_page():
    return jsonify([i.__dict__ for i in GetMyTransaction()])


@app.route("/status", methods=["GET"])
def status_page():
    return jsonify(Status())


def start():
    """
    Start the API server.
    """

    parser = argparse.ArgumentParser(
        description="This is an open source decentralized application network. In this network, you can develop and publish decentralized applications."
    )

    parser.add_argument("-p", "--port", type=int, help="Add new UNL node")

    args = parser.parse_args()

    if len(sys.argv) < 2:
        serve(app, host="0.0.0.0", port=8000)
    else:
        serve(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    start()
