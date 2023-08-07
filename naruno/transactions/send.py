#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time
from hashlib import sha256
from urllib import parse
from urllib import request
from urllib.request import urlopen

from naruno.accounts.get_balance import GetBalance
from naruno.accounts.get_sequence_number import GetSequanceNumber
from naruno.blockchain.block.get_block import GetBlock
from naruno.lib.log import get_logger
from naruno.lib.settings_system import the_settings
from naruno.transactions.get_transaction import GetTransaction
from naruno.transactions.transaction import Transaction
from naruno.wallet.ellipticcurve.ecdsa import Ecdsa
from naruno.wallet.ellipticcurve.privateKey import PrivateKey
from naruno.wallet.wallet_import import wallet_import

logger = get_logger("TRANSACTIONS")


line_before
new_code
line_after