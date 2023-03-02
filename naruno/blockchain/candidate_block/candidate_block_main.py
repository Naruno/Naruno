#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from decentra_network.transactions.transaction import Transaction
class candidate_block:
    """
    The candidate_block class.

    candidate_block class consists of 2 elements:
      * A list element for candidate_blocks
      * A list element for candidate_block_hashes
    """

    def __init__(
        self, candidate_blocks: list = None, candidate_block_hashes: list = None
    ):

        self.candidate_blocks = []
        self.candidate_block_hashes = []
        self.candidate_blocks.extend(candidate_blocks)
        self.candidate_block_hashes.extend(candidate_block_hashes)

        #turn list items json dumps
        for i in range(len(self.candidate_blocks)):
            self.candidate_blocks[i] = json.dumps(self.candidate_blocks[i])
        for i in range(len(self.candidate_block_hashes)):
            self.candidate_block_hashes[i] = json.dumps(self.candidate_block_hashes[i])

        self.candidate_blocks = list(dict.fromkeys(self.candidate_blocks))
        self.candidate_block_hashes = list(dict.fromkeys(self.candidate_block_hashes))

        #turn list items json dumps
        for i in range(len(self.candidate_blocks)):
            self.candidate_blocks[i] = json.loads(self.candidate_blocks[i])
        for i in range(len(self.candidate_block_hashes)):
            self.candidate_block_hashes[i] = json.loads(self.candidate_block_hashes[i])


        for block in self.candidate_blocks:
            temp_tx = [
                Transaction.load_json(element)
                for element in block["transaction"]
            ]
            block["transaction"] = temp_tx