#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import argparse
import os
import sys
from urllib.parse import unquote_plus

from flasgger import Swagger
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask import Response
from waitress import serve

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from decentra_network.accounts.get_balance import GetBalance
from decentra_network.blockchain.block.create_block import CreateBlock
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.consensus.consensus_main import consensus_trigger
from decentra_network.lib.export import export_the_transactions
from decentra_network.lib.log import get_logger
from decentra_network.lib.perpetualtimer import perpetualTimer
from decentra_network.lib.safety import safety_check
from decentra_network.lib.settings_system import (debug_mode, test_mode,
                                                  the_settings)
from decentra_network.lib.status import Status
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
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
swagger = Swagger(app)


@app.route("/")
def index():
    return redirect("/apidocs", code=302)


@app.route("/wallet/print", methods=["GET"])
def print_wallets_page():
    """
    Print wallets.
    ---
    definitions:
      wallet_list:
        type: string
      error:
        type: string
    responses:
      200:
        description: A list of wallets
        schema:
          $ref: '#/definitions/wallet_list'
        examples:
          "0": "wallet_address - CURRENTLY USED"
      500:
        description: A problem occurred
        schema:
          $ref: '#/definitions/error'
        examples:
          error: "A problem occurred"
    """

    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(print_wallets())


@app.route("/wallet/change/<number>", methods=["GET"])
def wallet_change_page(number):
    """
    Changes the current wallet.
    ---
    parameters:
      - name: number
        in: path
        type: integer
        required: true
    definitions:
      wallet_list:
        type: string
      error:
        type: string
    responses:
      200:
        description: A list of wallets
        schema:
          $ref: '#/definitions/wallet_list'
        examples:
          "0": "wallet_address - CURRENTLY USED"
      500:
        description: A problem occurred
        schema:
          $ref: '#/definitions/error'
        examples:
          error: "A problem occurred"
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    if wallet_selector(number):
        return jsonify(print_wallets())
    else:
        return Response(jsonify({"error": "A problem occurred"}), status=500)


@app.route("/wallet/create/<password>", methods=["GET"])
def create_wallet_page(password):
    """
    Creates a new wallet.
    ---
    parameters:
      - name: password
        in: path
        type: string
        required: true
    definitions:
      wallet_list:
        type: string
      error:
        type: string
    responses:
      200:
        description: A list of wallets
        schema:
          $ref: '#/definitions/wallet_list'
        examples:
          "0": "wallet_address - CURRENTLY USED"
      500:
        description: A problem occurred
        schema:
          $ref: '#/definitions/error'
        examples:
          error: "A problem occurred"
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    wallet_create(password)
    return jsonify(print_wallets())


@app.route("/wallet/delete", methods=["GET"])
def delete_wallets_page():
    """
    Delete current wallet.
    ---
    definitions:
      wallet_list:
        type: string
      error:
        type: string
    responses:
      200:
        description: A list of wallets
        schema:
          $ref: '#/definitions/wallet_list'
        examples:
          "0": "wallet_address - CURRENTLY USED"
      500:
        description: A problem occurred
        schema:
          $ref: '#/definitions/error'
        examples:
          error: "A problem occurred"
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    if delete_current_wallet():
        return jsonify(print_wallets())
    else:
        return Response(jsonify({"error": "A problem occurred"}), status=500)


@app.route("/send/coin/<address>/<amount>/<password>", methods=["GET"])
def send_coin_page(address, amount, password):
    """
    Creates a new wallet.
    ---
    parameters:
      - name: address
        in: path
        type: string
        required: true
      - name: amount
        in: path
        type: number
        required: true
      - name: password
        in: path
        type: string
        required: true
    definitions:
      success:
        type: string
      error:
        type: string
    responses:
      200:
        description: A list of wallets
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
      500:
        description: A problem occurred
        schema:
          $ref: '#/definitions/error'
        examples:
          error: "A problem occurred"
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    block = GetBlock()
    send_tx = send(block, password, address, amount)
    if send_tx != False:
        SavetoMyTransaction(send_tx)
        server.send_transaction(send_tx)
        SaveBlock(block)
        return jsonify("OK")
    else:
        return Response(jsonify({"error": "A problem occurred"}), status=500)


@app.route("/send/coin-data/<address>/<amount>/<data>/<password>",
           methods=["GET"])
def send_coin_data_page(address, amount, data, password):
    """
    Creates a new wallet.
    ---
    parameters:
      - name: address
        in: path
        type: string
        required: true
      - name: amount
        in: path
        type: number
        required: true
      - name: data
        in: path
        type: string
        required: true
      - name: password
        in: path
        type: string
        required: true
    definitions:
      success:
        type: string
      error:
        type: string
    responses:
      200:
        description: A list of wallets
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
      500:
        description: A problem occurred
        schema:
          $ref: '#/definitions/error'
        examples:
          error: "A problem occurred"
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    block = GetBlock()
    send_tx = send(block, password, address, amount, data)
    if send_tx != False:
        SavetoMyTransaction(send_tx)
        server.send_transaction(send_tx)
        SaveBlock(block)
        return jsonify("OK")
    else:
        return Response(jsonify({"error": "A problem occurred"}), status=500)


@app.route("/wallet/balance", methods=["GET"])
def balance_wallets_page():
    """
    Print wallets.
    ---
    definitions:
      balance:
        type: string
    responses:
      200:
        description: Balance of current wallet
        schema:
          $ref: '#/definitions/balance'
        examples:
          2000
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(GetBalance(GetBlock(), wallet_import(-1, 0)))


@app.route("/node/start/<ip>/<port>", methods=["GET"])
def node_start_page(ip, port):
    """
    Start a node.
    ---
    parameters:
      - name: ip
        in: path
        type: string
        required: true
      - name: port
        in: path
        type: number
        required: true
    definitions:
      success:
        type: string
    responses:
      200:
        description: Start a node
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    server(str(ip), int(port))
    return jsonify("OK")


@app.route("/node/stop", methods=["GET"])
def node_stop_page():
    """
    Stop a node.
    ---
    definitions:
      balance:
        type: string
    responses:
      200:
        description: Stop a node.
        schema:
          $ref: '#/definitions/balance'
        examples:
          OK
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    server.Server.stop()
    return jsonify("OK")


@app.route("/node/connect/<ip>/<port>", methods=["GET"])
def node_connect_page(ip, port):
    """
    Start a node.
    ---
    parameters:
      - name: ip
        in: path
        type: string
        required: true
      - name: port
        in: path
        type: number
        required: true
    definitions:
      success:
        type: string
      error:
        type: string
    responses:
      200:
        description: Start a node
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
      500:
        description: A problem occurred
        schema:
          $ref: '#/definitions/error'
        examples:
          error: "A problem occurred"
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    if server.Server.connect(str(ip), int(port)):
        return jsonify("OK")
    else:
        return Response(jsonify({"error": "A problem occurred"}), status=500)


@app.route("/node/connectmixdb", methods=["GET"])
def node_connectmixdb_page():
    """
    Node connect to mixdb.
    ---
    definitions:
      balance:
        type: string
    responses:
      200:
        description: Node connect to mixdb.
        schema:
          $ref: '#/definitions/balance'
        examples:
          OK
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    server.connectionfrommixdb()
    return jsonify("OK")


@app.route("/node/newunl/", methods=["GET"])
def node_newunl_page():
    """
    Add a new unl node.
    ---
    parameters:
      - name: node_id
        in: query
        type: string
        required: true
    definitions:
      success:
        type: string
    responses:
      200:
        description: Start a node
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
    """

    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.query_string}"
    )
    request.query_string = request.query_string.decode("utf-8")
    if "node_id=" in request.query_string:
        request.query_string = unquote_plus(request.query_string).replace(
            "node_id=", "")
    Unl.save_new_unl_node(request.query_string)
    return jsonify("OK")


@app.route("/node/id", methods=["GET"])
def node_id_page():
    """
    Shows node id.
    ---
    definitions:
      node_id:
        type: string
    responses:
      200:
        description: Start a node
        schema:
          $ref: '#/definitions/node_id'
        examples:
          node_id_test
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(server.id)


@app.route("/settings/test/on", methods=["GET"])
def settings_test_on_page():
    """
    Turn on test mode.
    ---
    definitions:
      success:
        type: string
    responses:
      200:
        description: Turn on test mode
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    test_mode(True)
    return jsonify("OK")


@app.route("/settings/test/off", methods=["GET"])
def settings_test_off_page():
    """
    Turn off test mode.
    ---
    definitions:
      success:
        type: string
    responses:
      200:
        description: Turn off test mode
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    test_mode(False)
    return jsonify("OK")


@app.route("/settings/debug/on", methods=["GET"])
def settings_debug_on_page():
    """
    Turn on debug mode.
    ---
    definitions:
      success:
        type: string
    responses:
      200:
        description: Turn on debug mode
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    app.config["DEBUG"] = True
    debug_mode(True)
    return jsonify("OK")


@app.route("/settings/debug/off", methods=["GET"])
def settings_debug_off_page():
    """
    Turn off debug mode.
    ---
    definitions:
      success:
        type: string
    responses:
      200:
        description: Turn off debug mode
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    app.config["DEBUG"] = False
    debug_mode(False)
    return jsonify("OK")


@app.route("/block/get", methods=["GET"])
def block_get_page():
    """
    Get a block.
    ---
    definitions:
      success:
        type: string
    responses:
      200:
        description: Get a block.
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    if the_settings()["test_mode"]:
        the_block = CreateBlock()
        SaveBlock(the_block)
        server.Server.send_block_to_other_nodes()
        logger.info("Consensus timer is started")
        perpetualTimer(the_block.consensus_timer, consensus_trigger)
    else:
        server.Server.send_me_full_block()
    return jsonify("OK")


@app.route("/export/transactions/csv", methods=["GET"])
def export_transaction_csv_page():
    """
    Export transactions to csv.
    ---
    definitions:
      success:
        type: string
      error:
        type: string
    responses:
      200:
        description: Export transactions to csv.
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
      500:
        description: A problem occurred
        schema:
          $ref: '#/definitions/error'
        examples:
          error: "A problem occurred"
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    if export_the_transactions():
        return jsonify("OK")
    else:
        return Response(jsonify({"error": "A problem occurred"}), status=500)


@app.route("/export/transactions/json", methods=["GET"])
def export_transaction_json_page():
    """
    Export transactions to json.
    ---
    definitions:
      success:
        type: string
      error:
        type: string
    responses:
      200:
        description: Export transactions to json.
        schema:
          $ref: '#/definitions/success'
        examples:
          OK
      500:
        description: A problem occurred
        schema:
          $ref: '#/definitions/error'
        examples:
          error: "A problem occurred"
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(
        [f"{str(i[0].__dict__)} | {str(i[1])}" for i in GetMyTransaction()])


@app.route("/status", methods=["GET"])
def status_page():
    """
    Shows status.
    ---
    definitions:
      status:
        type: string
    responses:
      200:
        description: Show status
        schema:
          $ref: '#/definitions/status'
        examples:
          OK
    """
    logger.info(
        f"{request.remote_addr} {request.method} {request.url} {request.data}")
    return jsonify(Status())


def start():
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

    safety_check(args.interface, args.timeout)

    logger.info(f"Starting API on port {args.port}")
    serve(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    start()
