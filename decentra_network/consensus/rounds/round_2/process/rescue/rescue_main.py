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
import random

from decentra_network.blockchain.block.block_main import Block
from decentra_network.lib.log import get_logger
from decentra_network.node.client.client import client
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl

logger = get_logger("CONSENSUS_SECOND_ROUND")


def rescue_main(
    block: Block,
    candidate_block_hash: dict,
    custom_server: server = None,
    custom_unl: client = None,
) -> Block:
    sender = candidate_block_hash["sender"]
    logger.warning(
        f"Our block is not valid, the system will try to get true block from decentra_network.node {sender}"
    )
    block.dowload_true_block = sender
    unl_list = Unl.get_as_node_type([sender])
    the_server = server.Server if custom_server is None else custom_server
    the_unl_node = random.choice(
        unl_list) if custom_unl is None else custom_unl
    the_server.send_client(the_unl_node, {"action": "sendmefullblock"})
    return block
