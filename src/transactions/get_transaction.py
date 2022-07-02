
#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from transactions.check.check_transaction import CheckTransaction

def GetTransaction(block, the_transaction):
    if CheckTransaction(block, the_transaction):
        block.pendingTransaction.append(the_transaction)
        from node.node import Node
        Node.send_transaction(the_transaction)
        block.save_block()
        return True
    else:
        return False