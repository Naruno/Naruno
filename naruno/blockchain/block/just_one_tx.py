#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from urllib.request import urlopen

from naruno.blockchain.block.get_block import GetBlock
from naruno.lib.log import get_logger
from naruno.lib.settings_system import the_settings
from naruno.transactions.pending.get_pending import GetPendingLen

logger = get_logger("BLOCKCHAIN")


def GetJustOneTX(block=None, ):
    if not the_settings()["baklava"]:
        block = block if block is not None else GetBlock()
        just_one_tx = block.just_one_tx
    else:
        just_one_tx = (
            urlopen("http://test_net.1.naruno.org:8000/blockjustonetx/get/"
                    ).read().decode("utf-8")).lower()

        if "true" in just_one_tx:
            just_one_tx = True
        else:
            just_one_tx = False

    return just_one_tx
