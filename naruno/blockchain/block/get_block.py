#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import os

from naruno.blockchain.block.block_main import Block
from naruno.config import TEMP_BLOCK_PATH
from naruno.consensus.rounds.round_1.process.transactions.checks.duplicated import Remove_Duplicates
from naruno.lib.config_system import get_config
from naruno.lib.log import get_logger

logger = get_logger("BLOCKCHAIN")


def GetBlock(custom_TEMP_BLOCK_PATH=None, get_normal_block=False, dont_clean=False):
    """
    Returns the block.
    """
    logger.info("Getting block from disk")

    the_TEMP_BLOCK_PATH = (TEMP_BLOCK_PATH if custom_TEMP_BLOCK_PATH is None
                           else custom_TEMP_BLOCK_PATH)

    os.chdir(get_config()["main_folder"])

    highest_the_TEMP_BLOCK_PATH = the_TEMP_BLOCK_PATH
    highest_number = 0

    highest_second_number = 0
    highest_other_high_number = 0
    for file in os.listdir("db/"):
        if ("db/" + file).startswith(the_TEMP_BLOCK_PATH) and not ("db/" + file) == the_TEMP_BLOCK_PATH:
            number = int((("db/" + file).replace(the_TEMP_BLOCK_PATH, "")).split("-")[1]) #seq
            high_number = int((("db/" + file).replace(the_TEMP_BLOCK_PATH, "")).split("-")[3]) #val
            other_high_number = int((("db/" + file).replace(the_TEMP_BLOCK_PATH, "")).split("-")[2]) #val

            # Write a code for getting the blocks with high number
            if number > highest_number:
                highest_number = number
                highest_the_TEMP_BLOCK_PATH = "db/" + file
                highest_second_number = high_number
                highest_other_high_number = other_high_number
            elif number == highest_number:
                if high_number > highest_second_number:
                    highest_number = number
                    highest_the_TEMP_BLOCK_PATH = "db/" + file
                    highest_second_number = high_number
                    highest_other_high_number = other_high_number
                elif high_number == highest_second_number:
                    if other_high_number > highest_other_high_number:
                        highest_number = number
                        highest_the_TEMP_BLOCK_PATH = "db/" + file
                        highest_second_number = high_number
                        highest_other_high_number = other_high_number
            
                


    logger.debug("Highest block: " + highest_the_TEMP_BLOCK_PATH)


    result_normal = Block("non")

    with contextlib.suppress(json.decoder.JSONDecodeError):
        with open(the_TEMP_BLOCK_PATH, "r") as block_file:
            the_block_json = json.load(block_file)
            result_normal = Block.load_json(the_block_json)


    with open(highest_the_TEMP_BLOCK_PATH, "r") as block_file:
        the_block_json = json.load(block_file)
        result_highest = Block.load_json(the_block_json)

    result_normal = Remove_Duplicates(result_normal)
    result_highest = Remove_Duplicates(result_highest)

    result_normal.validating_list = sorted(result_normal.validating_list,
                                   key=lambda x: x.fromUser)    

    result_highest.validating_list = sorted(result_highest.validating_list,
                                   key=lambda x: x.fromUser)    

    if get_normal_block:
        return result_normal

    if result_normal.sequence_number + result_normal.empty_block_number > result_highest.sequence_number + result_highest.empty_block_number:
        return result_normal
    elif result_normal.sequence_number + result_normal.empty_block_number == result_highest.sequence_number + result_highest.empty_block_number:

        result_normal_situation = 0
        result_highest_situation = 0
        if result_normal.round_1:
            result_normal_situation += 1
        if result_normal.round_2:
            result_normal_situation += 1

        if result_highest.round_1:
            result_highest_situation += 1
        if result_highest.round_2:
            result_highest_situation += 1


        if len(result_normal.validating_list) > len(result_highest.validating_list):

                return result_normal
        else:

                return result_highest

        
    else:
        return result_highest


