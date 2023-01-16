#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import os
import time

from decentra_network.accounts.account import Account
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash_part
from decentra_network.config import TEMP_BLOCK_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger
from decentra_network.blockchain.block.block_main import Block

logger = get_logger("BLOCKCHAIN")


def SaveBlock(
    block: Block,
    custom_TEMP_BLOCK_PATH=None,
    custom_TEMP_ACCOUNTS_PATH=None,
    custom_TEMP_BLOCKSHASH_PATH=None,
    custom_TEMP_BLOCKSHASH_PART_PATH=None,
    delete_old_validating_list=False,
    just_save_normal=False
):
    """
    Saves the current block to the TEMP_BLOCK_PATH.
    """
    logger.info("Saving block to disk")
    if block.first_time:
        SaveAccounts(
            Account(block.creator, block.coin_amount),
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
        )
        SaveBlockshash(
            block.previous_hash,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
        )
        SaveBlockshash_part(
            [block.previous_hash],
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        block.first_time = False
    the_TEMP_BLOCK_PATH = (TEMP_BLOCK_PATH if custom_TEMP_BLOCK_PATH is None
                           else custom_TEMP_BLOCK_PATH)
    secondly_situation = 0
    if block.round_1:
        secondly_situation += 1
    if block.round_2:
        secondly_situation += 1
    highest_the_TEMP_BLOCK_PATH = the_TEMP_BLOCK_PATH + "-" + str(block.sequence_number) + "-" + str(len(block.validating_list)) + "-" + str(secondly_situation)

    if delete_old_validating_list:
        os.chdir(get_config()["main_folder"])
        for file in os.listdir("db/"):
            if ("db/" + file).startswith(the_TEMP_BLOCK_PATH) and not ("db/" + file) == the_TEMP_BLOCK_PATH:
                number = int((("db/" + file).replace(the_TEMP_BLOCK_PATH, "")).split("-")[1])
                high_number = int((("db/" + file).replace(the_TEMP_BLOCK_PATH, "")).split("-")[2])
                if number == block.sequence_number and high_number != len(block.validating_list):
                    with contextlib.suppress(FileNotFoundError):
                        os.remove("db/" + file)

    if secondly_situation == 2:
            with contextlib.suppress(FileNotFoundError):
                os.remove(the_TEMP_BLOCK_PATH + "-" + str(block.sequence_number) + "-" + str(len(block.validating_list)) + "-" + str(1))
            with contextlib.suppress(FileNotFoundError):
                os.remove(the_TEMP_BLOCK_PATH + "-" + str(block.sequence_number) + "-" + str(len(block.validating_list)) + "-" + str(0))

    if secondly_situation == 1:
            with contextlib.suppress(FileNotFoundError):
                os.remove(the_TEMP_BLOCK_PATH + "-" + str(block.sequence_number) + "-" + str(len(block.validating_list)) + "-" + str(0))
            with contextlib.suppress(FileNotFoundError):
                os.remove(the_TEMP_BLOCK_PATH + "-" + str(block.sequence_number) + "-" + str(len(block.validating_list)) + "-" + str(2))
    
    if secondly_situation == 0:
            with contextlib.suppress(FileNotFoundError):
                os.remove(the_TEMP_BLOCK_PATH + "-" + str(block.sequence_number) + "-" + str(len(block.validating_list)) + "-" + str(1))
            with contextlib.suppress(FileNotFoundError):
                os.remove(the_TEMP_BLOCK_PATH + "-" + str(block.sequence_number) + "-" + str(len(block.validating_list)) + "-" + str(2))


    os.chdir(get_config()["main_folder"])
    with open(the_TEMP_BLOCK_PATH, "w") as block_file:
        json.dump(block.dump_json(), block_file)
    if not just_save_normal:
        with open(highest_the_TEMP_BLOCK_PATH, "w") as block_file:
            json.dump(block.dump_json(), block_file)