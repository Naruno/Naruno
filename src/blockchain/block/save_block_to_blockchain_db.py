#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import sqlite3

from config import BLOCKCHAIN_PATH


def saveBlockstoBlockchainDB(block):
    """
    Adds the existing block to the blockchain database
    at BLOCKCHAIN_PATH.
    """

    db = sqlite3.connect(BLOCKCHAIN_PATH)
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS blockchain(
                    previous_hash,
                    sequance_number,
                    hash
                );""")

    cur.execute(f"""INSERT INTO blockchain VALUES (
        '{block.previous_hash}', '{block.sequance_number}', '{block.hash}'
    )""")

    cur.execute(f"""CREATE TABLE accounts{block.sequance_number}(
                    PublicKey,
                    sequance_number,
                    balance
                );""")

    for each_account in block.Accounts:
        cur.execute(f"""INSERT INTO accounts{block.sequance_number} VALUES (?,?,?)""",
            [
                each_account.PublicKey,
                each_account.sequance_number,
                each_account.balance
            ]
        )
    cur.execute(f"""CREATE TABLE transactions{block.sequance_number}(
                    sequance_number,
                    signature,
                    fromUser,
                    toUser,
                    data,
                    amount,
                    transaction_fee
                );""")
    for each_transaction in block.validating_list:
        cur.execute(f"""INSERT INTO transactions{block.sequance_number} VALUES (?,?,?,?,?,?,?)""",
            [
                each_transaction.sequance_number,
                each_transaction.signature,
                each_transaction.fromUser,
                each_transaction.toUser,
                each_transaction.data,
                each_transaction.amount,
                each_transaction.transaction_fee
            ]
        )

    db.commit()
    db.close()
