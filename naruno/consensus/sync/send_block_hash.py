#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.blockchain.block.block_main import Block
from naruno.lib.log import get_logger
from naruno.node.server.server import server

logger = get_logger("CONSENSUS")


def send_block_hash(
    block: Block,
    the_server: server = None,
    send_block_hash_error: bool = False,
):
    logger.debug("Our block hash is sending to the unl nodes")
    try:
        the_server.send_my_block_hash(block)
        if send_block_hash_error:
            raise Exception("Block hash sending error")
    except Exception as e:
        logger.error(f"Block hash sending error: {e}")
