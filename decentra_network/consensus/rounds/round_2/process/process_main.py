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
import time

from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.candidate_block.candidate_block_main import (
    candidate_block,
)

from decentra_network.consensus.rounds.round_2.process.candidate_blocks_hashes.candidate_blocks_hashes_main import (
    process_candidate_blocks_hashes,
)
from decentra_network.consensus.rounds.round_2.process.rescue.rescue_main import (
    rescue_main,
)
from decentra_network.consensus.rounds.round_2.process.validate.validate_main import (
    validate_main,
)
from decentra_network.lib.log import get_logger


logger = get_logger("CONSENSUS_SECOND_ROUND")


def round_process(block: Block, candidate_class: candidate_block, unl_nodes: dict):

    candidate_block_hash = process_candidate_blocks_hashes(
        block, candidate_class, unl_nodes
    )

    if block.hash == candidate_block_hash["hash"]:
        validate_main(block)
    else:
        rescue_main(block, candidate_block_hash, unl_nodes)

    SaveBlock(block)
