#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
import zipfile
from hashlib import sha256
from zipfile import ZipFile

from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.blockchain.block.blocks_hash import GetBlockshash
from decentra_network.blockchain.block.blocks_hash import GetBlockshash_part
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.get_block_from_blockchain_db import \
    GetBlockstoBlockchainDB
from decentra_network.blockchain.block.hash.calculate_hash import CalculateHash
from decentra_network.config import BLOCKS_PATH
from decentra_network.config import EXTRACTED_PROOFS_PATH
from decentra_network.config import MY_TRANSACTION_PATH
from decentra_network.config import PROOF_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.lib.mix.merkle_root import MerkleTree
from decentra_network.transactions.transaction import Transaction


def CheckProof(
    proof,
    custom_TEMP_BLOCKSHASH_PART_PATH=None,
) -> bool:
    os.chdir(get_config()["main_folder"])

    splitted_proof = proof.split(".")
    temp = splitted_proof[0]
    the_proof_path = EXTRACTED_PROOFS_PATH + temp

    # Create a folder for the proof if it doesn't exist
    if not os.path.exists(the_proof_path):
        # Create the folder
        os.makedirs(the_proof_path)

    try:
        zip_file = zipfile.ZipFile(proof, "r")
    except FileNotFoundError:
        return None
    zip_file.extractall(the_proof_path)
    zip_file.close()

    the_proof_path = the_proof_path + "/" + "db/"
    for file in os.listdir(the_proof_path):
        print(the_proof_path + file)
        if os.path.isdir(the_proof_path + file):
            the_proof_path = the_proof_path + file + "/"

    print(the_proof_path)
    full_blockshash_path = None
    sequance_number = None
    for file in os.listdir(the_proof_path):
        if file.endswith(".blockshash_full.json"):
            full_blockshash_path = the_proof_path + file
        if file.endswith(".block.json"):
            splitted_name = file.split(".")
            sequance_number = splitted_name[0]

    result_2 = GetBlockstoBlockchainDB(
        sequance_number=sequance_number,
        custom_BLOCKS_PATH=the_proof_path,
    )

    Saved_blocks_hash = GetBlockshash(
        custom_TEMP_BLOCKSHASH_PATH=full_blockshash_path)

    hash_2 = CalculateHash(
        result_2[0],
        result_2[3],
        result_2[2],
        result_2[1],
    )

    the_hash_part = MerkleTree([Saved_blocks_hash[0], hash_2]).getRootHash()

    the_blockshash_part = GetBlockshash_part(
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)

    is_in = False
    for i in the_blockshash_part:
        if i == the_hash_part:
            is_in = True
    return is_in
