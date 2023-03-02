#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
from hashlib import sha256
from zipfile import ZipFile

from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.get_block_from_blockchain_db import \
    GetBlockstoBlockchainDB
from decentra_network.config import BLOCKS_PATH
from decentra_network.config import MY_TRANSACTION_PATH
from decentra_network.config import PROOF_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.transactions.transaction import Transaction


def GetProof(
    signature: str,
    custom_PROOF_PATH=None,
    custom_BLOCKS_PATH=None,
    custom_TEMP_ACCOUNTS_PATH=None,
    custom_TEMP_BLOCKSHASH_PATH=None,
    custom_TEMP_BLOCKSHASH_PART_PATH=None,
) -> str:

    the_PROOF_PATH = PROOF_PATH if custom_PROOF_PATH is None else custom_PROOF_PATH

    the_BLOCKS_PATH = BLOCKS_PATH if custom_BLOCKS_PATH is None else custom_BLOCKS_PATH

    os.chdir(get_config()["main_folder"])
    sequence_number = None

    for file in os.listdir(the_BLOCKS_PATH):
        if file.endswith(".block.json"):
            with open(the_BLOCKS_PATH + file, "r") as block_file:
                the_block_json = json.load(block_file)
            for transaction in the_block_json["validating_list"]:
                if transaction["signature"] == signature:
                    sequence_number = file.split(".")[0]

    if sequence_number is None:
        return None

    result = GetBlockstoBlockchainDB(
        sequence_number,
        custom_BLOCKS_PATH=the_BLOCKS_PATH,
        custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
        custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
    )
    full_blockshash_sequence_number = result[0].sequence_number + (
        result[0].part_amount - result[0].sequence_number)

    full_blockshash_path = (the_BLOCKS_PATH +
                            str(full_blockshash_sequence_number - 1) +
                            ".blockshash_full.json")

    block_path = the_BLOCKS_PATH + str(sequence_number) + ".block.json"
    account_path = the_BLOCKS_PATH + str(sequence_number) + ".accounts.db"
    blockshash_path = the_BLOCKS_PATH + str(
        sequence_number) + ".blockshash.json"
    blockshashpart_path = (the_BLOCKS_PATH + str(sequence_number) +
                           ".blockshashpart.json")

    proof_path = (the_PROOF_PATH + sha256(
        (signature).encode("utf-8")).hexdigest() + ".proof.zip")

    with ZipFile(proof_path, "w") as zip:
        zip.write(full_blockshash_path)
        zip.write(block_path)
        zip.write(account_path)
        zip.write(blockshash_path)
        zip.write(blockshashpart_path)

    return proof_path
