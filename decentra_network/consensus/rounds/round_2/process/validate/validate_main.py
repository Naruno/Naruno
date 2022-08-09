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

from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.consensus.rounds.round_1.checks.checks_main import round_check
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.lib.log import get_logger
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl

from decentra_network.consensus.rounds.round_2.checks.checks_main import round_check

from decentra_network.blockchain.candidate_block.candidate_block_main import (
    candidate_block,
)
from decentra_network.blockchain.block.block_main import Block

from decentra_network.consensus.rounds.round_2.process.rescue.rescue_main import (
    rescue_main,
)

from decentra_network.consensus.rounds.round_2.process.candidate_blocks_hashes.candidate_blocks_hashes_main import (
    process_candidate_blocks_hashes,
)

logger = get_logger("CONSENSUS_SECOND_ROUND")


def validate_main(block: Block):
    logger.info("Block approved")
    block.validated = True
    block.validated_time = int(time.time())
    block.round_2 = True
