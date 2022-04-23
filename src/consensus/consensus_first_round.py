#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from blockchain.block.calculate_hash import CalculateHash
from blockchain.candidate_block.get_candidate_blocks import GetCandidateBlocks
from lib.log import get_logger
from node.node import Node
from node.unl import Unl
from transactions.process_the_transaction import ProccesstheTransaction
from transactions.send_transaction_to_the_block import \
    SendTransactiontoTheBlock

logger = get_logger("CONSENSUS_FIRST_ROUND")


def consensus_round_1(block):
    """
    At this stage of the consensus process,
    The transactions of our and the unl nodes
    are evaluated and transactions accepted by
    owned by more than 50 percent.
    Inputs:
      * block: The block (class) we want consensus
      round 1 to be done
    """

    logger.info(
        f"BLOCK#{block.sequance_number}:{block.empty_block_number} First round is starting"
    )

    unl_nodes = Unl.get_unl_nodes()
    if not block.raund_1_node:
        logger.info("Our block is sending to the unl nodes")
        Node.main_node.send_my_block(Unl.get_as_node_type(unl_nodes))
        block.raund_1_node = True
        block.save_block()
    candidate_class = GetCandidateBlocks()
    if len(candidate_class.candidate_blocks) > ((len(unl_nodes) * 80) / 100):
        logger.info("Enough candidate blocks received")

        if not (int(time.time()) -
                block.raund_1_starting_time) < block.raund_1_time:
            logger.info("True time")
            temp_validating_list = []
            for candidate_block in candidate_class.candidate_blocks[:]:
                logger.debug(f"Candidate block {str(candidate_block)}")

                for other_block_tx in candidate_block["transaction"]:

                    tx_valid = 0

                    for my_txs in block.validating_list:
                        if other_block_tx.signature == my_txs.signature:
                            tx_valid += 1

                    if len(candidate_class.candidate_blocks) != 1:

                        for other_block in candidate_class.candidate_blocks[:]:
                            if candidate_block["signature"] != other_block[
                                    "signature"]:

                                for other_block_txs in other_block[
                                        "transaction"]:
                                    if (other_block_tx.signature ==
                                            other_block_txs.signature):

                                        tx_valid += 1
                    else:
                        tx_valid += 1

                    logger.debug(
                        f"Tx valid of {other_block_tx.signature} : {tx_valid}")
                    if tx_valid > (len(unl_nodes) / 2):

                        already_in_ok = False
                        for alrady_tx in temp_validating_list[:]:

                            if other_block_tx.signature == alrady_tx.signature:
                                logger.warning(
                                    "The transaction is already in the list")
                                already_in_ok = True
                        if not already_in_ok:
                            logger.info(
                                f"Transaction is valid ({other_block_tx.signature})"
                            )
                            temp_validating_list.append(other_block_tx)

            newly_added_list = []

            for my_validating_list in block.validating_list[:]:
                ok = False
                for my_temp_validating_list in temp_validating_list[:]:
                    if (my_validating_list.signature ==
                            my_temp_validating_list.signature):
                        ok = True
                block.validating_list.remove(my_validating_list)
                if not ok:
                    newly_added_list.append(my_validating_list)

            block.validating_list = temp_validating_list
            logger.debug(f"Newly validating list {block.validating_list}")

            for each_newly in newly_added_list:
                SendTransactiontoTheBlock(
                    block,
                    each_newly.sequance_number,
                    each_newly.signature,
                    each_newly.fromUser,
                    each_newly.toUser,
                    each_newly.transaction_fee,
                    each_newly.data,
                    each_newly.amount,
                    transaction_sender=None,
                    transaction_time=each_newly.transaction_time,
                )

            block.raund_1 = True

            block.raund_2_starting_time = int(time.time())

            ProccesstheTransaction(block)

            block.hash = CalculateHash(block)
            logger.debug(f"Block hash {block.hash}")

            block.save_block()

        else:
            if not block.decrease_the_time == 3:
                logger.info("Decrease the time")
                block.decrease_the_time += 1
                block.increase_the_time = 0
                block.save_block()

    else:
        if not (int(time.time()) -
                block.raund_1_starting_time) < block.raund_1_time:
            if not block.increase_the_time == 3:
                logger.info("Increase the time")
                block.increase_the_time += 1
                block.decrease_the_time = 0
                block.save_block()

    logger.info("First round is done")
