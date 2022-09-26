#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from decentra_network.lib.performance_analyzers.accounts import \
    Accounts_IO_Performance_Analyzer
from decentra_network.lib.performance_analyzers.block import \
    Block_IO_Performance_Analyzer
from decentra_network.lib.performance_analyzers.blockshash import \
    Blockshash_IO_Performance_Analyzer
from decentra_network.lib.performance_analyzers.blockshash_part import \
    Blockshash_part_IO_Performance_Analyzer
from decentra_network.lib.performance_analyzers.transactions import \
    Transactions_IO_Performance_Analyzer


def heartbeat_generic_db_analyzer():
    the_block = Block_IO_Performance_Analyzer()
    the_accounts = Accounts_IO_Performance_Analyzer()
    the_blockshash = Blockshash_IO_Performance_Analyzer()
    the_blockshash_part = Blockshash_part_IO_Performance_Analyzer()
    the_transactions = Transactions_IO_Performance_Analyzer()

    the_block_analysis = the_block.analyze()
    the_accounts_analysis = the_accounts.analyze()
    the_blockshash_analysis = the_blockshash.analyze()
    the_blockshash_part_analysis = the_blockshash_part.analyze()
    the_transactions_analysis = the_transactions.analyze()

    save_total = (the_block_analysis[0] + the_accounts_analysis[0] +
                  the_blockshash_analysis[0] +
                  the_blockshash_part_analysis[0] +
                  the_transactions_analysis[0])
    get_total = (the_block_analysis[1] + the_accounts_analysis[1] +
                 the_blockshash_analysis[1] + the_blockshash_part_analysis[1] +
                 the_transactions_analysis[1])
    size_total = (the_block_analysis[2] + the_accounts_analysis[2] +
                  the_blockshash_analysis[2] +
                  the_blockshash_part_analysis[2] +
                  the_transactions_analysis[2])

    return [
        [
            save_total,
            get_total,
            size_total,
        ],
        [
            save_total - the_blockshash_part_analysis[0],
            get_total - the_blockshash_part_analysis[1],
            size_total - the_blockshash_part_analysis[2],
        ],
    ]


if __name__ == "__main__":
    print(heartbeat_generic_db_analyzer())
