#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.blocks_hash import GetBlockshash
from decentra_network.blockchain.block.blocks_hash import GetBlockshash_part
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash_part
from decentra_network.blockchain.block.hash.calculate_hash import CalculateHash
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.lib.log import get_logger
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.get_transaction import GetTransaction
from decentra_network.transactions.process_the_transaction import ProccesstheTransaction

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
    logger.info("Our block is sending to the unl nodes")
    nodes = Unl.get_as_node_type(unl_nodes)
    server.Server.send_my_block(block)
    candidate_class = GetCandidateBlocks(custom_nodes_list=nodes)
    time_difference = int(time.time()) - block.raund_1_starting_time
    logger.info(f"candidate block number {len(candidate_class.candidate_blocks)} limit {len(unl_nodes) * 80 / 100}")
    if len(candidate_class.candidate_blocks) > ((len(unl_nodes) * 80) / 100):
        logger.info("Enough candidate blocks received")

        logger.info(f"Time difference is {time_difference}")
        logger.info(f"block.raund_1_time is {block.raund_1_time}")

        if time_difference > block.raund_1_time:
            logger.info("True time")
            temp_validating_list = []
            for candidate_block in candidate_class.candidate_blocks[:]:
                logger.debug(f"Candidate block {str(candidate_block)}")

                for other_block_tx in candidate_block["transaction"]:

                    tx_valid = sum(
                        other_block_tx.signature == my_txs.signature
                        for my_txs in block.validating_list
                    )

                    if len(candidate_class.candidate_blocks) != 1:

                        for other_block in candidate_class.candidate_blocks[:]:
                            if candidate_block["signature"] != other_block["signature"]:

                                for other_block_txs in other_block["transaction"]:
                                    if (
                                        other_block_tx.signature
                                        == other_block_txs.signature
                                    ):

                                        tx_valid += 1
                    else:
                        tx_valid += 1

                    logger.debug(f"Tx valid of {other_block_tx.signature} : {tx_valid}")
                    if tx_valid > (len(unl_nodes) / 2):

                        already_in_ok = False
                        for alrady_tx in temp_validating_list[:]:

                            if other_block_tx.signature == alrady_tx.signature:
                                logger.warning("The transaction is already in the list")
                                already_in_ok = True
                        if not already_in_ok:
                            logger.info(
                                f"Transaction is valid ({other_block_tx.signature})"
                            )
                            temp_validating_list.append(other_block_tx)

            newly_added_list = []

            for my_validating_list in block.validating_list[:]:
                ok = any(
                    (my_validating_list.signature == my_temp_validating_list.signature)
                    for my_temp_validating_list in temp_validating_list[:]
                )

                block.validating_list.remove(my_validating_list)
                if not ok:
                    newly_added_list.append(my_validating_list)

            block.validating_list = temp_validating_list
            logger.debug(f"Newly validating list {block.validating_list}")

            for each_newly in newly_added_list:
                if GetTransaction(block, each_newly):
                    server.send_transaction(each_newly)

            block.raund_1 = True

            block.raund_2_starting_time = int(time.time())

            account_list = GetAccounts()
            ProccesstheTransaction(block, account_list)
            SaveAccounts(account_list)

            part_of_blocks_hash = GetBlockshash_part()
            the_blocks_hash = GetBlockshash()
            the_accounts = GetAccounts()
            CalculateHash(block, part_of_blocks_hash, the_blocks_hash, the_accounts)

            SaveAccounts(the_accounts)
            SaveBlockshash_part(part_of_blocks_hash)
            SaveBlockshash(the_blocks_hash)

            logger.debug(f"Block hash {block.hash}")

            SaveBlock(block)

    logger.info("First round is done")
