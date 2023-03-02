#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.lib.log import get_logger
from decentra_network.wallet.ellipticcurve.ecdsa import Ecdsa
from decentra_network.wallet.ellipticcurve.publicKey import PublicKey
from decentra_network.wallet.ellipticcurve.signature import Signature

logger = get_logger("TRANSACTIONS")


def Check_Sign(transaction):
    """
    Check if the transaction signature is valid
    """

    if Ecdsa.verify(
        (str(transaction.sequence_number) + str(transaction.fromUser) +
         str(transaction.toUser) + str(transaction.data) +
         str(transaction.amount) + str(transaction.transaction_fee) +
         str(transaction.transaction_time)),
            Signature.fromBase64(transaction.signature),
            PublicKey.fromPem(transaction.fromUser),
    ):
        pass
    else:
        logger.debug("The signature is not valid")
        return False

    return True
