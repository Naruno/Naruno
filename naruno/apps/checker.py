#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import time

from naruno.accounts.commanders.delete_commander import DeleteCommander
from naruno.lib.log import get_logger

logger = get_logger("REMOTE_APP")


def checker(integration, logger=logger):
    """
    Retrieves new transactions, checks if they match previously sent
    transactions, and resends any transactions that have not been
    validated. Uses a combination of loops and try/except blocks to
    iterate over transactions and catch any errors that may occur.

    Args:
        integration: The Integration object instance

    Returns:
        None
    """

    try:
        logger.debug("Starting checker function")

        # Sleep for a certain amount of time
        time.sleep(integration.wait_amount)

        # Get new transactions
        new_txs = integration.get(
            get_all=True,
            disable_caches=True,
            from_thread=True,
            disable_sended_not_validated=True,
            force_sended=True,
        )

        # Log how many new transactions were retrieved
        logger.debug(f"Retrieved {len(new_txs)} new transactions")

        # Loop through previously sent transactions and check if they have been validated
        for sended_tx in integration.sended_txs[:integration.max_tx_number //
                                                2]:
            in_get = False
            with contextlib.suppress(ValueError):
                # If the transaction has been validated, remove it from the list of sent transactions
                integration.sended_txs.remove(sended_tx)

            # Check if the validated transaction matches the sent transaction
            for vaidated_tx in new_txs:
                if (vaidated_tx["toUser"] == sended_tx[2]
                        and vaidated_tx["data"]["action"] == json.loads(
                            sended_tx[6])["action"]
                        and vaidated_tx["data"]["app_data"] == json.loads(
                            sended_tx[6])["app_data"]):
                    in_get = True
            if not in_get:
                # If the validated transaction does not match the sent transaction, resend the transaction
                logger.warning(
                    f"Transaction not found, resending: {sended_tx}")

                integration.send(
                    sended_tx[0],
                    sended_tx[1],
                    sended_tx[2],
                    sended_tx[3],
                    sended_tx[4],
                    sended_tx[5],
                )

        logger.debug("Exiting checker function")

    except Exception as e:
        # Catch any errors that occur during the function and log them
        logger.error(f"An error occured in the checker function: {e}")
