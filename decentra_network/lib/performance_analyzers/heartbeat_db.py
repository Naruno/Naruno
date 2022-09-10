#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from cgitb import reset
import contextlib
import hashlib
import os
import sys
import time

from speed_calculator import calculate

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..",".."))


from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock


from decentra_network.accounts.account import Account
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts


from decentra_network.blockchain.block.blocks_hash import GetBlockshash
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash

from decentra_network.blockchain.block.blocks_hash import GetBlockshash_part
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash_part


class Block_IO_Performance_Analyzer():
    """
    This class is used to analyze the performance of GetBlock
    """
    def __init__(self):
        self.block = Block("test")
        self.block.first_time = False

        self.block.hash = hashlib.sha256("test".encode()).hexdigest()
        self.block.round_2_starting_time = time.time()
        self.block.validated_time = time.time()

    def analyze(self) -> float:
        """
        This function is used to analyze the performance of GetBlock
        """

        result = calculate(self.save_operation), calculate(self.get_operation), os.path.getsize("db/Block_Performance_Analyzer_block.pf") / 1000000

        os.remove("db/Block_Performance_Analyzer_block.pf")

        return result

    def save_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """
        SaveBlock(
            self.block,
            custom_TEMP_BLOCK_PATH = "db/Block_Performance_Analyzer_block.pf",
            )

    def get_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        GetBlock("db/Block_Performance_Analyzer_block.pf")







class Accounts_IO_Performance_Analyzer():
    """
    This class is used to analyze the performance of GetBlock
    """
    def __init__(self):
        self.block = Block("test")

        self.account = Account("test", 5000)


        self.the_account_list = []


        for i in range(self.block.max_tx_number):
            self.the_account_list.append(self.account)        


    def analyze(self) -> float:
        """
        This function is used to analyze the performance of GetBlock
        """

        result = calculate(self.save_operation), calculate(self.get_operation), os.path.getsize("db/Accounts_Performance_Analyzer_accounts.pf") / 1000000

        
        os.remove("db/Accounts_Performance_Analyzer_accounts.pf")

        return result

    def save_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        SaveAccounts(self.the_account_list, custom_TEMP_ACCOUNTS_PATH = "db/Accounts_Performance_Analyzer_accounts.pf")


    def get_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        the_accounts = GetAccounts("db/Accounts_Performance_Analyzer_accounts.pf")





class Blockshash_IO_Performance_Analyzer():
    """
    This class is used to analyze the performance of GetBlock
    """
    def __init__(self):
        self.block = Block("test")
        the_hash = hashlib.sha256("test".encode()).hexdigest()
        self.blocks_hash = [the_hash for i in range(self.block.part_amount)] 
        self.blocks_hash.append(self.block.previous_hash)


        


    def analyze(self) -> float:
        """
        This function is used to analyze the performance of GetBlock
        """

        result = calculate(self.save_operation), calculate(self.get_operation), os.path.getsize("db/Blockshash_Performance_Analyzer_blockshash.pf") / 1000000

        
        os.remove("db/Blockshash_Performance_Analyzer_blockshash.pf")

        return result

    def save_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        SaveBlockshash(self.blocks_hash, custom_TEMP_BLOCKSHASH_PATH = "db/Blockshash_Performance_Analyzer_blockshash.pf")


    def get_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        GetBlockshash(custom_TEMP_BLOCKSHASH_PATH = "db/Blockshash_Performance_Analyzer_blockshash.pf")


class Blockshash_part_IO_Performance_Analyzer():
    """
    This class is used to analyze the performance of GetBlock
    """
    def __init__(self):
        self.block = Block("test")
        the_hash = hashlib.sha256("test".encode()).hexdigest()

        # calculate the seconds in a day
        seconds_in_a_day = 60 * 60 * 24

        # how many blocks in a day
        blocks_in_a_day = seconds_in_a_day / self.block.block_time

        # how many blocks in a year
        blocks_in_a_year = blocks_in_a_day * 365



        self.blocks_hash = [the_hash for i in range(int(blocks_in_a_year))] 


    def analyze(self) -> float:
        """
        This function is used to analyze the performance of GetBlock
        """

        result = calculate(self.save_operation), calculate(self.get_operation), os.path.getsize("db/Blockshash_part_Performance_Analyzer_blockshash.pf") / 1000000

        
        os.remove("db/Blockshash_part_Performance_Analyzer_blockshash.pf")

        return result

    def save_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        SaveBlockshash_part(self.blocks_hash, custom_TEMP_BLOCKSHASH_PART_PATH = "db/Blockshash_part_Performance_Analyzer_blockshash.pf")


    def get_operation(self):
        """
        This function is used to analyze the performance of GetBlock
        """

        GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH = "db/Blockshash_part_Performance_Analyzer_blockshash.pf")




if __name__ == "__main__":
    the_block = Block_IO_Performance_Analyzer()
    the_accounts = Accounts_IO_Performance_Analyzer()
    the_blockshash = Blockshash_IO_Performance_Analyzer()
    the_blockshash_part = Blockshash_part_IO_Performance_Analyzer()

    the_block_analysis = the_block.analyze()
    the_accounts_analysis = the_accounts.analyze()
    the_blockshash_analysis = the_blockshash.analyze()
    the_blockshash_part_analysis = the_blockshash_part.analyze()
    

    print("Block    (Save, Get, Size(MB)): ", the_block_analysis)
    print("Accounts (Save, Get, Size(MB)): ", the_accounts_analysis)
    print("Blockshash (Save, Get, Size(MB)): ", the_blockshash_analysis)
    print("--------------------------------")
    print(f"Blockshash_part after 1 year (calculated in every {the_blockshash_part.block.part_amount} block) (Save, Get, Size(MB)): ", the_blockshash_part_analysis)
    print("--------------------------------")
    print("Total heartbeats save: ", the_block_analysis[0] + the_accounts_analysis[0] + the_blockshash_analysis[0])
    print("Total heartbeats get: ", the_block_analysis[1] + the_accounts_analysis[1] + the_blockshash_analysis[1])