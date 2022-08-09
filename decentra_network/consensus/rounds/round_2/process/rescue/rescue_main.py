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

from decentra_network.blockchain.candidate_block.candidate_block_main import candidate_block
from decentra_network.blockchain.block.block_main import Block

logger = get_logger("CONSENSUS_SECOND_ROUND")


def rescue_main(block: Block, candidate_block_hash: dict, unl_nodes: dict):

                        sender = candidate_block_hash["sender"]
                        logger.warning(
                            f"Our block is not valid, the system will try to get true block from decentra_network.node {sender}"
                        )
                        node = server.Server
                        unl_list = Unl.get_as_node_type([sender])
                        node.send_client(unl_list[0],  {"action":"sendmefullblock"})
                        block.dowload_true_block = sender