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

from naruno.accounts.account import Account
from naruno.accounts.save_accounts import SaveAccounts
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import SaveBlockshash
from naruno.blockchain.block.blocks_hash import SaveBlockshash_part
from naruno.config import TEMP_BLOCK_PATH
from naruno.consensus.rounds.round_1.process.transactions.checks.duplicated import \
    Remove_Duplicates
from naruno.lib.config_system import get_config
from naruno.lib.log import get_logger
from naruno.lib.settings_system import the_settings
from naruno.transactions.cleaner import Cleaner
from naruno.transactions.pending.get_pending import GetPending

logger = get_logger("BLOCKCHAIN")


def SaveBlock(
    block: Block,
    custom_TEMP_BLOCK_PATH=None,
    custom_TEMP_ACCOUNTS_PATH=None,
    custom_TEMP_BLOCKSHASH_PATH=None,
    custom_TEMP_BLOCKSHASH_PART_PATH=None,
    delete_old_validating_list=False,
    just_save_normal=False,
    dont_clean=False,
):
    """
    Saves the current block to the TEMP_BLOCK_PATH.
    """
    if not dont_clean:
        cleaned = Cleaner(block, pending_list_txs=GetPending())
        block.validating_list = cleaned[0]

        block = Remove_Duplicates(block)
        block.validating_list = sorted(block.validating_list,
                                       key=lambda x: x.fromUser)

    logger.info("Saving block to disk")
    logger.debug(
        f"Block#{block.sequence_number + block.empty_block_number}:{block.empty_block_number}: {block.dump_json()}"
    )
    if block.first_time:
        accounts_list = [Account(block.creator, block.coin_amount)]
        baklava_test_net_users = [
            Account("55de207a538855b4da2d60325e8afadc3b3caa04",
                    block.minumum_transfer_amount + block.transaction_fee * 100),

            Account("2f58be5d152490affa05a7b0fd3cef8c195dae6d",
                    block.minumum_transfer_amount + block.transaction_fee * 100),
            Account("a26536e07f3c2a850fb2b63cbe99d84589674634",
                    block.minumum_transfer_amount + block.transaction_fee * 100),
            Account("0be5c9cd8bf68cafeec3a2d5d51678923780d3ff",
                    block.minumum_transfer_amount + block.transaction_fee * 100),
            Account("82d87a6bfd279d30ad4894912eae2efacd4d46d6",
                    block.minumum_transfer_amount + block.transaction_fee * 100),
            Account("f6e4955a8077ae5ed7d95014b41f22dcee6c0d76",
                    block.minumum_transfer_amount + block.transaction_fee * 100),
            Account("73672aafc1890fc18d9b88105380b396eca799a5",
                    block.minumum_transfer_amount + block.transaction_fee * 100),
            Account("83a15e056f98305418ee9ea26caf664c3d020040",
                    block.minumum_transfer_amount + block.transaction_fee * 100),       
            Account("b1df8deda30d4f88cb905ecd57ed0fc7f2021d00",
                    block.minumum_transfer_amount + block.transaction_fee * 100),  
            Account("ec29c2e01987796a3677da2e3a9b4a098b93b89a",
                    block.minumum_transfer_amount + block.transaction_fee * 100),  
            Account("887af3d44bfe39005b4cc480c2b03a11c2fb8b63",
                    block.minumum_transfer_amount + block.transaction_fee * 100),  
            Account("17d3d3e20bd84ddf6e3ed85fa693c12654f174eb",
                    block.minumum_transfer_amount + block.transaction_fee * 100),  
            Account("00db4cebdeb9c8588dc9e1ffbe918d80dcf2ce97",
                    block.minumum_transfer_amount + block.transaction_fee * 100),  

            Account("1da75d769ab3604abc04763d20dc3f70bf1c69b8",
                    block.minumum_transfer_amount + block.transaction_fee * 100),                                                                                                                                                                                                                                                                                 
        ]
        if the_settings()["baklava"]:
            accounts_list.extend(baklava_test_net_users)
        SaveAccounts(
            accounts_list,
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
    highest_the_TEMP_BLOCK_PATH = (the_TEMP_BLOCK_PATH + "-" +
                                   str(block.sequence_number + block.empty_block_number) + "-" +
                                   str(len(block.validating_list)) + "-" +
                                   str(secondly_situation) + "-" +
                                   str(time.time()))
    logger.info(f"Saving block to {highest_the_TEMP_BLOCK_PATH}")

    if delete_old_validating_list:
        os.chdir(get_config()["main_folder"])
        for file in os.listdir("db/"):
            if ("db/" + file).startswith(the_TEMP_BLOCK_PATH) and not (
                    "db/" + file) == the_TEMP_BLOCK_PATH:
                number = int((("db/" + file).replace(the_TEMP_BLOCK_PATH,
                                                     "")).split("-")[1])
                high_number = int(
                    (("db/" + file).replace(the_TEMP_BLOCK_PATH,
                                            "")).split("-")[2])
                secondly_situation_number = int(
                    (("db/" + file).replace(the_TEMP_BLOCK_PATH,
                                            "")).split("-")[3])
                if (number == block.sequence_number + block.empty_block_number
                        and high_number != len(block.validating_list)
                        and secondly_situation_number == 1):
                    with contextlib.suppress(FileNotFoundError):
                        logger.info(f"Deleting old validating list: {file}")
                        os.remove("db/" + file)

    for file in os.listdir("db/"):
        if ("db/" + file).startswith(the_TEMP_BLOCK_PATH) and not (
                "db/" + file) == the_TEMP_BLOCK_PATH:
            number = int((("db/" + file).replace(the_TEMP_BLOCK_PATH,
                                                 "")).split("-")[1])  # seq
            high_number = int(
                (("db/" + file).replace(the_TEMP_BLOCK_PATH,
                                        "")).split("-")[2])  # val
            if number < block.sequence_number + block.empty_block_number:
                with contextlib.suppress(FileNotFoundError):
                    logger.info("Removing " + "db/" + file)
                    os.remove("db/" + file)

    with open(the_TEMP_BLOCK_PATH, "w") as block_file:
        json.dump(block.dump_json(), block_file)
    if not just_save_normal:
        with open(highest_the_TEMP_BLOCK_PATH, "w") as block_file:
            json.dump(block.dump_json(), block_file)
