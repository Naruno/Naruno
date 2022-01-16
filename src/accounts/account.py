#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import hashlib
import json
import pickle
import os

from lib.config_system import get_config

from config import TEMP_ACCOUNTS_PATH, TEMP_ACCOUNTS_PART_PATH


class Account:
    """
    The account Class.

    Account class consists of 3 elements:
      * PublicKey: Public key created with ECDSA.
      * sequance_number: Makes each transaction single use,
        incrementing 1 after each transaction.
      * balance: The amount of dnc coins of account.
    """

    def __init__(self, PublicKey, balance, sequance_number=0):
        self.Address = PublicKey

        self.sequance_number = sequance_number
        self.balance = balance

    def get_hash(self, encoding="ascii"):
        """
        Returns sha256 created with all the elements of the account.
        """
        account_data = json.dumps(self.dump_json()).encode(encoding)
        return hashlib.sha256(account_data).hexdigest()

    def dump_json(self):
        """
        Converts and returns the account's elements to json,
        which can then be loaded with the load_json () function.
        """
        data = {
            "address": self.Address,
            "balance": self.balance,
            "sequence_number": self.sequance_number,
        }
        return data

    @staticmethod
    def load_json(data):
        """
        Json returns data in the appropriate format as the account class.
        """
        return Account(data["public_key"], data["balance"], data["sequence_number"])

    def __str__(self):
        return self.Address


def GetAccounts():
    os.chdir(get_config()["main_folder"])
    if not os.path.exists(TEMP_ACCOUNTS_PATH):
        return []
    else:
        with open(TEMP_ACCOUNTS_PATH, "rb") as block_file:
            return pickle.load(block_file)


def GetAccounts_part():
    os.chdir(get_config()["main_folder"])
    if not os.path.exists(TEMP_ACCOUNTS_PART_PATH):
        return []
    else:
        with open(TEMP_ACCOUNTS_PART_PATH, "rb") as block_file:
            return pickle.load(block_file)
