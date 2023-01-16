#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.blockchain.block.block_main import Block
from decentra_network.lib.log import get_logger
from decentra_network.transactions.transaction import Transaction

logger = get_logger("BLOCKCHAIN")


def shares(block: Block, custom_shares=None, custom_fee_address=None) -> list:
    """
    It returns the transactions that needed for locked shares distribution.
    """
    logger.info("Share distribution started.")
    the_shares = block.shares if custom_shares is None else custom_shares
    the_fee_address = (block.fee_address
                       if custom_fee_address is None else custom_fee_address)
    logger.debug(f"block.sequence_number: {block.sequence_number}")
    logger.debug(f"the_shares: {the_shares}")
    logger.debug(f"the_fee_address: {the_fee_address}")

    tx_list = []

    the_time = block.start_time
    logger.debug(f"the_time: {the_time}")

    for share in the_shares:
        rate = block.sequence_number / share[2]
        if rate.is_integer() and rate != 0.0:
            if not block.sequence_number > share[3]:
                tx_list.append(
                    Transaction(
                        0,
                        "DN",
                        "DNB",
                        share[0],
                        "NP",
                        share[1],
                        0,
                        the_time,
                    ))

    fee = 0
    for tx in block.validating_list:
        fee += tx.transaction_fee
    if fee > 0:
        tx_list.append(
            Transaction(
                0,
                "DN",
                "DNA",
                the_fee_address,
                "NP",
                fee,
                0,
                the_time,
            ))

    return tx_list
