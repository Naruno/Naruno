#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from decentra_network.lib.log import get_logger

logger = get_logger("CONSENSUS_SECOND_ROUND")


def process_candidate_blocks_hashes(block: Block,
                                    candidate_class: candidate_block,
                                    unl_nodes: dict) -> dict:
    logger.info("Control process of candidate block hashes is started.")

    current_hash = {"signature": "A", "hash": False, "previous_hash": False}
    previous_hash = {"signature": "A", "hash": False, "previous_hash": False}

    for candidate_block_hash in candidate_class.candidate_block_hashes[:]:
        logger.debug(f"Candidate block hash {candidate_block_hash}")

        tx_valid = 1

        for other_block in candidate_class.candidate_block_hashes[:]:
            if (candidate_block_hash != other_block
                    and candidate_block_hash["hash"] == other_block["hash"]):
                tx_valid += 1

        logger.debug(f"Hash valid of  {candidate_block_hash} : {tx_valid}")

        if tx_valid > (((len(unl_nodes)+1) * 50) / 100):
            logger.info(
                f"candidate_block_hash: {candidate_block_hash} is validated.")
            current_hash = candidate_block_hash

    for candidate_block_hash in candidate_class.candidate_block_hashes[:]:
        logger.debug(f"Candidate block hash previous_hash {candidate_block_hash}")

        tx_valid = 1

        for other_block in candidate_class.candidate_block_hashes[:]:
            if (candidate_block_hash != other_block
                    and candidate_block_hash["previous_hash"] == other_block["previous_hash"]):
                tx_valid += 1
        logger.debug(f"Hash valid of previous_hash  {candidate_block_hash} : {tx_valid}")
        if tx_valid > (((len(unl_nodes)+1) * 50) / 100):
            logger.info(
                f"candidate_block_hash previous_hash: {candidate_block_hash} is validated.")
            previous_hash = candidate_block_hash



    if current_hash != {"signature": "A", "hash": False, "previous_hash": False} or previous_hash != {"signature": "A", "hash": False, "previous_hash": False}:
        if current_hash["signature"] == "self":
            for other in candidate_class.candidate_block_hashes[:]:
                if current_hash != other and current_hash["hash"] == other["hash"]:
                    current_hash = other
                    break
                    
        if previous_hash["signature"] == "self":
            for other in candidate_class.candidate_block_hashes[:]:
                if previous_hash != other and previous_hash["previous_hash"] == other["previous_hash"]:
                    previous_hash = other
                    break        
        return {"hash": current_hash, "previous_hash": previous_hash}

    logger.debug("All candidate_block_hashes can not be validated.")
    return {"hash": {"hash": False}, "previous_hash": {"previous_hash": False}}
