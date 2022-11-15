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
    for candidate_block_hash in candidate_class.candidate_block_hashes[:]:
        logger.debug(f"Candidate block hash {candidate_block_hash}")

        tx_valid = 1

        for other_block in candidate_class.candidate_block_hashes[:]:
            if (candidate_block_hash != other_block
                    and candidate_block_hash["hash"] == other_block["hash"]):
                tx_valid += 1
                logger.debug(
                    f"candidate_block_hash: {candidate_block_hash} validated from {other_block}"
                )
        logger.debug(f"Hash valid of  {candidate_block_hash} : {tx_valid}")
        logger.info(
            f"candidate_block_hash: {candidate_block_hash} is validated.")
        if tx_valid >= ((len(unl_nodes) * 80) / 100):
            logger.info(
                f"candidate_block_hash: {candidate_block_hash} is validated.")
            return candidate_block_hash
    logger.warning("All candidate_block_hashes can not be validated.")
    return {"hash": False}
