#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time
from hashlib import sha256

from naruno.accounts.get_balance import GetBalance
from naruno.accounts.get_sequence_number import GetSequanceNumber
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.get_block import GetBlock
from naruno.lib.log import get_logger
from naruno.lib.settings_system import the_settings
from naruno.transactions.get_transaction import GetTransaction
from naruno.transactions.transaction import Transaction
from naruno.wallet.ellipticcurve.ecdsa import Ecdsa
from naruno.wallet.ellipticcurve.privateKey import PrivateKey
from naruno.wallet.wallet_import import wallet_import


from urllib.request import urlopen
from urllib import request, parse


logger = get_logger("TRANSACTIONS")


def send(
    password,
    to_user,
    amount=None,
    data="",
    block=None,
    custom_current_time=None,
    custom_sequence_number=None,
    custom_balance=None,
    custom_account_list=None,
    custom_set_sequence_number=None,
):
    """
    The main function for sending the transaction.

    Inputs:
        password: The password of the wallet.
        to_user: The address of the recipient.
        amount: The amount of the transaction.
        data: The data of the transaction.

    """
    if (wallet_import(int(the_settings()["wallet"]),
                      2) == sha256(password.encode("utf-8")).hexdigest()):

        my_private_key = wallet_import(-1, 1, password)
        my_public_key = "".join([
            l.strip() for l in wallet_import(-1, 0).splitlines()
            if l and not l.startswith("-----")
        ])    
        if not the_settings()["baklava"]:
            block = block if block is not None else GetBlock()

            minumum_transfer_amount = block.minumum_transfer_amount
            max_data_size = block.max_data_size
            max_tx_number = block.max_tx_number
            transaction_fee = block.transaction_fee

            the_balance = GetBalance(to_user,
                        account_list=custom_account_list,
                        dont_convert=True,
                        block=block)
            sequence_number = GetSequanceNumber(my_public_key) + 1
        else:
            the_balance = float(urlopen(f"http://test_net.1.naruno.org:8000/balance/get/?address={to_user}").read().decode("utf-8").replace("\n", ""))
            sequence_number = float(urlopen(f"http://test_net.1.naruno.org:8000/sequence/get/?address={wallet_import(-1,3)}").read().decode("utf-8").replace("\n", "")) + 1


            transaction_fee = float(urlopen("http://test_net.1.naruno.org:8000/blocktransactionfee/get/").read().decode("utf-8"))
            max_tx_number = int(urlopen("http://test_net.1.naruno.org:8000/blockmaxtxnumber/get/").read().decode("utf-8"))
            max_data_size = int(urlopen("http://test_net.1.naruno.org:8000/blockmaxdatasize/get/").read().decode("utf-8"))
            minumum_transfer_amount = int(urlopen("http://test_net.1.naruno.org:8000/blockminumumtransferamount/get/").read().decode("utf-8"))

        if custom_set_sequence_number is not None:
            sequence_number = custom_set_sequence_number

        the_minumum_amount = 0
        if (the_balance >= 0):
            pass
        else:
            the_minumum_amount = minumum_transfer_amount
        amount = amount if amount is not None else the_minumum_amount

        try:
            amount = float(amount)
        except ValueError:
            logger.exception("This is not float coin amount.")
            return False

        if amount < 0:
            logger.error("This is negative coin amount.")
            return False

        if (max_data_size / max_tx_number) < len(data):
            logger.error("The data is too long.")
            return False

        decimal_amount = len(str(transaction_fee).split(".")[1])
        if len(str(amount).split(".")[1]) > decimal_amount:
            logger.error(
                f"The amount of decimal places is more than {decimal_amount}.")
            return False




        # Get the current fee
        transaction_fee = transaction_fee

        tx_time = int(time.time())
        the_transaction = Transaction(
            sequence_number,
            "signature",
            my_public_key,
            to_user,
            data,
            amount,
            transaction_fee,
            tx_time,
        )
        the_transaction.signature = Ecdsa.sign(
                        (str(the_transaction.sequence_number) + the_transaction.fromUser + str(the_transaction.toUser) +
                        str(the_transaction.data)) + str(the_transaction.amount) + str(the_transaction.transaction_fee) +
                        str(the_transaction.transaction_time),
                        PrivateKey.fromPem(my_private_key),
                    ).toBase64()        
        logger.info(f"Transaction: {the_transaction.dump_json()}")

        sending_result = False

        if not the_settings()["baklava"]:
            sending_result = GetTransaction(
                    block,
                    the_transaction,
                    custom_current_time=custom_current_time,
                    custom_sequence_number=custom_sequence_number,
                    custom_balance=custom_balance,
                    custom_account_list=custom_account_list,
            )
        else:
            logger.info("Sending the transaction to the baklava network.")
            logger.info(f"Transaction: {the_transaction.dump_json()}")
            the_data = {
                "sequence_number": the_transaction.sequence_number,
                "signature": the_transaction.signature,
                "fromUser": the_transaction.fromUser,
                "toUser": the_transaction.toUser,
                "amount": the_transaction.amount,
                "data": the_transaction.data,
                "transaction_fee": the_transaction.transaction_fee,
                "time_of_transaction": the_transaction.transaction_time,
            }

            data = parse.urlencode(the_data).encode()
            req =  request.Request("http://test_net.1.naruno.org:8000/transaction/send/", data=data) # this will make the method "POST"
            try:
                resp = request.urlopen(req)
                sending_result = True
            except:
                sending_result = False

        if sending_result:

            del my_private_key
            del password

            return the_transaction
        else:
            logger.error("The transaction is not valid.")
            return False

    else:
        logger.error("Password is not correct")
        return False
