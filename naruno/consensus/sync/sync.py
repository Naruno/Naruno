#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import threading
import traceback
from naruno.blockchain.block.block_main import Block
from naruno.consensus.sync.send_block import send_block
from naruno.consensus.sync.send_block_hash import send_block_hash
from naruno.lib.log import get_logger
from naruno.node.server.server import server
import naruno
logger = get_logger("CONSENSUS")


sync_round_1 = True
sync_round_2 = False

sended_txs = []

def sync(
    block: Block,
    pending_list_txs: list = None,
    custom_server: server = None,
    send_block_error: bool = False,
    send_block_hash_error: bool = False,
    send_transaction_error: bool = False,
):
    """
    Data sending consists of 3 stages.
    Block sending,blockhash sending and transection.
    It shares the data of the existing chains with the nodes.
    """

    logger.info("Data sending process is starting")
    the_server = server.Server if custom_server is None else custom_server

    if naruno.consensus.sync.sync.sync_round_1:
        threading.Thread(
            target=send_block,
            args=(block, the_server, send_block_error),
        ).start()
        naruno.consensus.sync.sync.sync_round_1 = False
  
    if naruno.consensus.sync.sync.sync_round_2:
            threading.Thread(
                target=send_block_hash,
                args=(block, the_server, send_block_hash_error),
            ).start()
            naruno.consensus.sync.sync.sync_round_2 = False

    logger.debug("Transactions is sending to the unl nodes")
    the_transactions_list = copy.copy(block.validating_list)
    if pending_list_txs is not None:
        the_transactions_list += pending_list_txs
    for i in the_transactions_list:
        try:
            if not i.signature in naruno.consensus.sync.sync.sended_txs:
                naruno.consensus.sync.sync.sended_txs.append(i.signature)
                the_server.send_transaction(i)
            if send_transaction_error:
                raise Exception("Transaction sending error")
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Transaction sending error: {e}")
