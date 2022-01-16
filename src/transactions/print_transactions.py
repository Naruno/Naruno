#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from transactions.get_my_transaction import GetMyTransaction


def PrintTransactions():
    """
    Prints all transactions in my transaction.
    """

    print("\n")
    print(*[i.__dict__ for i in GetMyTransaction()], sep = "\n\n")
    print("\n")
