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
from decentra_network.lib.log import get_logger

logger = get_logger("CONSENSUS_SECOND_ROUND")


def validate_main(block: Block) -> Block:
    logger.info("Validating process is started")
    block.validated = True
    block.validated_time = int(time.time())
    block.round_2 = True
    logger.debug(f"block.validated: {block.validated}")
    logger.debug(f"block.validated_time: {block.validated_time}")
    logger.debug(f"block.round_2: {block.round_2}")

    return block
