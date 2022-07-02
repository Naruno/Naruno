#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from lib.log import get_logger
from wallet.ellipticcurve.ecdsa import Ecdsa
from wallet.ellipticcurve.publicKey import PublicKey
from wallet.ellipticcurve.signature import Signature

logger = get_logger("TRANSACTIONS")

def Check_Sign(transaction):
    """
    Check if the transaction signature is valid
    """

    if Ecdsa.verify(
        (str(transaction.sequance_number) + str(transaction.fromUser) +
         str(transaction.toUser) + str(transaction.data) +
         str(transaction.amount) + str(transaction.transaction_fee) +
         str(transaction.transaction_time)),
            Signature.fromBase64(transaction.signature),
            PublicKey.fromPem(transaction.fromUser),
    ):
        logger.info("The signature is valid")
    else:
        return False


    return True