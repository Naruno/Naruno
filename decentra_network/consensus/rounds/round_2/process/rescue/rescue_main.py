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
from decentra_network.lib.log import get_logger
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl

logger = get_logger("CONSENSUS_SECOND_ROUND")


def rescue_main(block: Block, candidate_block_hash: dict, unl_nodes: dict):

    sender = candidate_block_hash["sender"]
    logger.warning(
        f"Our block is not valid, the system will try to get true block from decentra_network.node {sender}"
    )
    node = server.Server
    unl_list = Unl.get_as_node_type([sender])
    node.send_client(unl_list[0], {"action": "sendmefullblock"})
    block.dowload_true_block = sender
