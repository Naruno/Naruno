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
from naruno.lib.kot import KOT
from naruno.lib.log import get_logger
from naruno.lib.settings_system import the_settings
from naruno.transactions.cleaner import Cleaner
from naruno.transactions.pending.get_pending import GetPending
import naruno

block_db = KOT("block_db", folder=get_config()["main_folder"] + "/db")

logger = get_logger("BLOCKCHAIN")



serial_testers = [
    "2844854d58334e66540097479439be65e0aa4efc",
    "7f53b1bb58032bc0212b8f1abc9fbb6510a16671",
    "8e0a8f580c43dd2b33d62afbfa514b3cbe262061",
    "0022b1a2c50249be6e760be4f3c2c0d9ed467fc3",
    "65abccda166c7f730376a0c15753942392b21d73",
    "c8ecc03e12e9b1975851ac4bac2159e2210c8402",

    "80df451fc2653ee4bb85230f2e9800f07527f778",

    "f51b88c59db9cac5e933ac8827bd7f10dc543ae3",

    "59bd07543a4aaf2e45a9b8b8f29e372de79d47ce",

    "7c697b908b77064d70ef4526a658eb9e2e5a9ee6",

    "5764cfd11addb37353c7e159a909e90f1de3c5e9",

    "e4ec7b50fe90c117ad37b41b01e5059c1c903ce0",

    "fd29f1d5b573796d4bd614c3c52738bbfcc5e340",

    "b01a9cdd81bad9cefc43733b5146c2a1b1b4dd6c",

    "c8dca04b72bc69b4e3ac3067f6d0174f2dcfe680",

    "755089190444e4af31aa4641c8d6e03254014b11",

    "68b777ebba65e8ab4af3d6bdb0837abc3ae177d9",

    "f641261d1527cade37371957afe04eb2d7e6b471",

    "7c7bf0510137fc29f09f2df2e38a45146567df7d",

    "1aa29b64943c955e2c1dfa5b734a5c617cdd4a8d",

    "d865a195c73d06313d72dcf3579d9920e4b4584b",

    "60d4357a85a2113467860455e5ccdb7b127a97dd",

    "bd679bd9bf83a00766cb0ae29ab0f9aae7f2d73e",

    "2b0d9405d9f8a6c658608dd2255528e0a12f4f16",

    "884aaa97c4121bbee5a3d79a312900c090bbbff5",

    "29b7ab3aeafedef1c3ad81323473ade7877ad698",

    "cc9ac91de747f657c1a2b6c9e071cf53833e357d",

    "52185af45f343636dcb2e88843a12e24aad3be9c",

    "73b02b4a4715c96eec46823b5fb1e1f401dcd1cb",

    "4b59062c6d3840a023fdc8aaa5c0a87f05aab62e",

    "8ed1aea1b9ebe2e4cfc9b9b03b53ac892bc63119",

    "6c9189efacd2c9b2bdbde200b5bae8cb022a9bd7",

    "ddf8a128b477f00167367f8d7e7816412c81feae",

    "58f9bda368fb61dcdc177af0daea1eb46b53ed5",

    "16bdffb8012f79c7818ee67054994fe128012cc4",
    "eae2c4f8ff12c10e0a3b0c8a5a677a2b9e50309e",

    "fcd23380b3ef500b205424c435837b8367e7e0a6",
    "1e65a85a0716c53fca521d7cbf9096d2f9a18ab4",

    "c010bb210da143a01d0d2ae914fd033c549e33c7",

    "1c8d4b723b67165847e3b11e3029748e6ebf5139",

    "b2345bda4ff22d0c51f27c4d470c63f63730ac77",

    "17008875dc5a6c9102a5c2aa1e03249d7f576237",

    "71fa49f318437ac5f3a72f6048f0f15dff974cce",

    "095fef5e67fad85a0cd40517d46316741f7b7e5c",

    "b1956275dadc0e91952b7991d692457c8699c73b",
    "d5a262b8719540b95e742838abf50a67c3972d82",

    "e493b8b92c3271af170064bcf42f706272bce631",

    "51a5563ecd11b49c19f2f11d3bb8ac1a0f75e4ea",

    "1243e02aa77ca080edd879b031fee5d2858ef248",

    "069f4682619925d4862c9597ac501c67b39e0608",

    "bdf78ffeed1cb2e37e2cd1e444ee6cf552b62e40",

    "6b31a60a3a73aa7b80b5a63fed63fcfdb85ee863",

    "a426fad6820c77d5d0c730c7f13bd1d668e17b45",

    "90f248e2d1143fd3995ebc2de856115d305ee46c",

    "6c3b4fd7a8f619194f13bacfb83bbeee91bf1ce0",

    "746c2ed9eae6210533854c217586b27330f80417",

    "329506e24ef995ec3e2759242ce52033a41be14a",

    "a02a508328575e913a09a9dd28a11145e62c9865",

    "9abb7a1219a20d6e55f8e4d5ae6ec0e89c2b4770",

    "1bb50e042ce653ec8501f47d712dc1ded0c6374a",

    "d3cbae4148f79953f5b86c8ab5c70282cbf398b7",





]
individuals = [
    "55de207a538855b4da2d60325e8afadc3b3caa04",


    "86e9a2454e2d2bd12f56ef37e39d026608013e72",


    "2f58be5d152490affa05a7b0fd3cef8c195dae6d",


    "a26536e07f3c2a850fb2b63cbe99d84589674634",


    "0be5c9cd8bf68cafeec3a2d5d51678923780d3ff",


    "82d87a6bfd279d30ad4894912eae2efacd4d46d6",


    "f6e4955a8077ae5ed7d95014b41f22dcee6c0d76",


    "73672aafc1890fc18d9b88105380b396eca799a5",


    "83a15e056f98305418ee9ea26caf664c3d020040",


    "b1df8deda30d4f88cb905ecd57ed0fc7f2021d00",


    "ec29c2e01987796a3677da2e3a9b4a098b93b89a",


    "887af3d44bfe39005b4cc480c2b03a11c2fb8b63",


    "17d3d3e20bd84ddf6e3ed85fa693c12654f174eb",


    "1da75d769ab3604abc04763d20dc3f70bf1c69b8",


    "d7eee170a14b99e37a3e3fc6d375d1d28bddf62b",


    "d7f20b7990cc593e248f1d0dd31dd7a235a40d9a",


    "75f7e0e090834c959f6538b1a4c80f03be410bdd",


    "d37cb2c0df30965f2bc12cea040386e70e32402b",


    "0af54b3f47fc1577688e7c2c227672f610cad292",


    "96bb7bac1af450ea0c17300ea4f61b1cd0b88b6d",


    "709bf017a48d2f02bb5d5d8d205ccf39d8205b4a",


    "5b943d77a8b7e66aa60b98a2197f2197db4f464b",


    "bba1e2f5871c02b130416229c02dd54fc404cd21",


    "dcf715a42784bfedf009b515ada46c1946a3339b",


    "0af54b3f47fc1577688e7c2c227672f610cad292",


    "0af54b3f47fc1577688e7c2c227672f610cad292",


    "0af54b3f47fc1577688e7c2c227672f610cad292",


    "cbdeeab5577f6f8693e571494e61dc0f356d9d09",


    "09375da881e7d546b8520a7e39160fc05eb60ce1",


    "b3232a5ed1d57c339fb3a258be40c51e221b48af",


    "7be509d428fc848485683a599cc4bbd958bd6df3",


    "2b76e7031353e9cbf62e2d259b54b98673f997c9",


    "614deef9abde68a0dab39fe5ee9f9cb2f9e8773a",


    "44281e3b85497d41d8c99f3b8b66a3e88e354ca1",


    "5db89649f397be7d3787cfca2e9f39245ef5f8e1",


    "b3e6e03b6c3f6ea8989177d23a9a055e2a05659b",


    "bc512bab30167fe84c84208be8759bf9839d7815",


    "138c27b39d5789319aa9a0c00262cb5360d146d0",


    "0dbe3d640ee1632b222154197a23319870f3d12d",


    "4a1b3198530952ee851722b105770ef21c59e472",


    "541cb5cc142e94aed187f83ee0d91a1470db3023",


    "caefad8f89b701d8087945780ad24fe0f993ae2f",


    "8f571575a492ef27f0fe02916303ea867f50876d",


    "508c9565bac49d318eb5c67f6e6e0354acbc4edf",


    "c7b71bd5100d2081de69497776064589e98c4fe1",


    "c58b9d12474108867f4a0924f4c521119a57d62f",


    "0d435e7fb86a46f4849a4eb41f683ab322f03d6b",


    "2E6A70110890b7A46F7857E2866023043CeF4680",


    "078e6dd15b33411462d284baf4c901cfd828558c",


    "88b73c67bf3aab4764d627cc9aa1150c6ae97794",


    "450305d3bb1a0fd7343824f136177220d436c046",


    "e7b72ca5af68bc5b8ddd98e4187c68efcfbec5cd",
]

specials = ["e087a455c3b35d5022491b380e3e34d68df4ca6c"]

special_testers = [
    "d78101e2cb261efab28ee54a0e6d716820a1bab1",
    "40a175793d9b7082157fd3e1632fc25c9f3f5234"
    ]


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
        baklava_test_net_users = []

        baklava_test_net_users.extend([Account(i,(2 * block.minumum_transfer_amount) +block.transaction_fee * 100,) for i in serial_testers])
        baklava_test_net_users.extend([Account(i,(2 * block.minumum_transfer_amount) +block.transaction_fee * 100,) for i in special_testers])
        baklava_test_net_users.extend([Account(i,(2 * block.minumum_transfer_amount) +block.transaction_fee * 100,) for i in individuals])
        baklava_test_net_users.extend([Account(i,(10 * block.minumum_transfer_amount) +block.transaction_fee * 100,) for i in specials])



        if the_settings()["baklava_users"]:
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
    highest_the_TEMP_BLOCK_PATH = (
        the_TEMP_BLOCK_PATH + "-" +
        str(block.sequence_number + block.empty_block_number) + "-" +
        str(len(block.validating_list)) + "-" + str(secondly_situation) + "-" +
        str(time.time()))
    logger.info(f"Saving block to {highest_the_TEMP_BLOCK_PATH}")

    if delete_old_validating_list:
        os.chdir(get_config()["main_folder"])
        for file in os.listdir("db/"):
            if ("db/" + file).startswith(the_TEMP_BLOCK_PATH) and not (
                    "db/" + file) == the_TEMP_BLOCK_PATH:
                with contextlib.suppress(IndexError):
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
                            block_db.delete("db/"+file)

    for file in os.listdir("db/"):
        if ("db/" + file).startswith(the_TEMP_BLOCK_PATH) and not (
                "db/" + file) == the_TEMP_BLOCK_PATH:
            with contextlib.suppress(IndexError):
                number = int((("db/" + file).replace(the_TEMP_BLOCK_PATH,
                                                     "")).split("-")[1])  # seq
                high_number = int(
                    (("db/" + file).replace(the_TEMP_BLOCK_PATH,
                                            "")).split("-")[2])  # val
                if number < block.sequence_number + block.empty_block_number:
                    with contextlib.suppress(FileNotFoundError):
                        logger.info("Removing " + "db/" + file)
                        block_db.delete("db/"+file)

    block_db_path_first = os.path.join(get_config()["main_folder"],
                                       the_TEMP_BLOCK_PATH)

    naruno.blockchain.block.get_block.the_ram_block[the_TEMP_BLOCK_PATH] = block
    block_db.set(the_TEMP_BLOCK_PATH,
                 block.dump_json(),
                 custom_key_location=block_db_path_first)

    if not just_save_normal:
        block_db_path_second = os.path.join(get_config()["main_folder"],
                                            highest_the_TEMP_BLOCK_PATH)
        block_db.set(highest_the_TEMP_BLOCK_PATH,
                     block.dump_json(),
                     custom_key_location=block_db_path_second)
