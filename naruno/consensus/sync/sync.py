#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import copy
import threading

from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.get_block import GetBlock
from naruno.blockchain.block.save_block import SaveBlock
from naruno.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from naruno.consensus.finished.finished_main import finished_main
from naruno.consensus.ongoing.ongoing_main import ongoing_main
from naruno.lib.log import get_logger
from naruno.lib.perpetualtimer import perpetualTimer
from naruno.node.client.client import client
from naruno.node.server.server import server
from naruno.transactions.cleaner import Cleaner
from naruno.transactions.pending.get_pending import GetPending

from naruno.consensus.sync.send_block import send_block
from naruno.consensus.sync.send_block_hash import send_block_hash

logger = get_logger("CONSENSUS")



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

    if not block.round_1:
        threading.Thread(
            target=send_block,
            args=(
                block, the_server, send_block_error
            ),
        ).start()

    else:
        if not block.round_2:
            threading.Thread(
                target=send_block_hash,
                args=(
                    block, the_server, send_block_hash_error
                ),
            ).start()

    logger.debug("Transactions is sending to the unl nodes")
    the_transactions_list = copy.copy(block.validating_list)
    if pending_list_txs is not None:
        the_transactions_list += pending_list_txs
    for i in the_transactions_list:
        try:
            the_server.send_transaction(i)
            if send_transaction_error:
                raise Exception("Transaction sending error")
        except Exception as e:
            logger.error(f"Transaction sending error: {e}")
