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
        if not block.round_1 and not block.round_2:
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
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),

            Account("2f58be5d152490affa05a7b0fd3cef8c195dae6d",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),
            Account("a26536e07f3c2a850fb2b63cbe99d84589674634",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),
            Account("0be5c9cd8bf68cafeec3a2d5d51678923780d3ff",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),
            Account("82d87a6bfd279d30ad4894912eae2efacd4d46d6",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),
            Account("f6e4955a8077ae5ed7d95014b41f22dcee6c0d76",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),
            Account("73672aafc1890fc18d9b88105380b396eca799a5",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),
            Account("83a15e056f98305418ee9ea26caf664c3d020040",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),       
            Account("b1df8deda30d4f88cb905ecd57ed0fc7f2021d00",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),  
            Account("ec29c2e01987796a3677da2e3a9b4a098b93b89a",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),  
            Account("887af3d44bfe39005b4cc480c2b03a11c2fb8b63",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),  
            Account("17d3d3e20bd84ddf6e3ed85fa693c12654f174eb",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),

            Account("1da75d769ab3604abc04763d20dc3f70bf1c69b8",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),    

            Account("d7eee170a14b99e37a3e3fc6d375d1d28bddf62b",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),  
            Account("d7f20b7990cc593e248f1d0dd31dd7a235a40d9a",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),  
            Account("75f7e0e090834c959f6538b1a4c80f03be410bdd",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),                                                              


            Account("d37cb2c0df30965f2bc12cea040386e70e32402b",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),   

            Account("0af54b3f47fc1577688e7c2c227672f610cad292",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),       






            Account("96bb7bac1af450ea0c17300ea4f61b1cd0b88b6d",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),   
            Account("709bf017a48d2f02bb5d5d8d205ccf39d8205b4a",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),   
            Account("5b943d77a8b7e66aa60b98a2197f2197db4f464b",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),   
            Account("bba1e2f5871c02b130416229c02dd54fc404cd21",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),   
            Account("dcf715a42784bfedf009b515ada46c1946a3339b",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),   
            Account("0af54b3f47fc1577688e7c2c227672f610cad292",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),   
            Account("0af54b3f47fc1577688e7c2c227672f610cad292",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),   
            Account("0af54b3f47fc1577688e7c2c227672f610cad292",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),                                                                                                                                               

            Account("cbdeeab5577f6f8693e571494e61dc0f356d9d09",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),


            Account("09375da881e7d546b8520a7e39160fc05eb60ce1",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),

            Account("b3232a5ed1d57c339fb3a258be40c51e221b48af",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),

            Account("7be509d428fc848485683a599cc4bbd958bd6df3",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),

            Account("2b76e7031353e9cbf62e2d259b54b98673f997c9",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),

            Account("614deef9abde68a0dab39fe5ee9f9cb2f9e8773a",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),

            Account("44281e3b85497d41d8c99f3b8b66a3e88e354ca1",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),

            Account("5db89649f397be7d3787cfca2e9f39245ef5f8e1",
                    (2 * block.minumum_transfer_amount) + block.transaction_fee * 100),


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
