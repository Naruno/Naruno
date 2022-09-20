#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.get_block_from_blockchain_db import GetBlockstoBlockchainDB

from decentra_network.config import MY_TRANSACTION_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.transactions.transaction import Transaction
from decentra_network.config import BLOCKS_PATH


from zipfile import ZipFile

def GetProof(tx, proof_path, custom_BLOCKS_PATH=None):

    the_BLOCKS_PATH = (BLOCKS_PATH if custom_BLOCKS_PATH is None else custom_BLOCKS_PATH)

    os.chdir(get_config()["main_folder"])
    sequance_number = None

    for file in os.listdir(the_BLOCKS_PATH):
        if file.endswith(".block.json"):
            with open(the_BLOCKS_PATH + file, "r") as block_file:
                the_block_json = json.load(block_file)
            for transaction in the_block_json["transactions"]:
                if transaction["hash"] == tx.hash:
                    sequance_number = file.split(".")[0]

    if sequance_number is None:
        return False

    result = GetBlockstoBlockchainDB(sequance_number)
    full_blockshash_sequance_number = (result[0].sequance_number + (result[0].sequance_number - result[0].part_amount))
    
    
    full_blockshash_path = (the_BLOCKS_PATH + str(full_blockshash_sequance_number) +
                         ".blockshash_full.json")

    block_path = (the_BLOCKS_PATH + str(sequance_number) + ".block.json")
    account_path = (the_BLOCKS_PATH + str(sequance_number) + ".accounts.db")
    blockshash_path = (the_BLOCKS_PATH + str(sequance_number) + ".blockshash.json")
    blockshashpart_path = (the_BLOCKS_PATH + str(sequance_number) + ".blockshashpart.json")
    

    with ZipFile(proof_path + tx.hash + ".proof.zip", "w") as zip:
        zip.write(full_blockshash_path)
        zip.write(block_path)
        zip.write(account_path)
        zip.write(blockshash_path)
        zip.write(blockshashpart_path)
    
    return True


