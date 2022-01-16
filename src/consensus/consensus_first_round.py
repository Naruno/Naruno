#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import time

from lib.mixlib import dprint

from node.unl import get_as_node_type, get_unl_nodes
from node.myownp2pn import mynode

from blockchain.candidate_block.get_candidate_blocks import GetCandidateBlocks
from blockchain.block.calculate_hash import CalculateHash

from transactions.process_the_transaction import ProccesstheTransaction
from transactions.create_transaction import CreateTransaction


def consensus_round_1(block):
        """
        At this stage of the consensus process,
        The transactions of our and the unl nodes 
        are evaluated and transactions accepted by 
        owned by more than 50 percent.
        Inputs:
          * block: The block (class) we want consensus 
          round 1 to be done
        """

        unl_nodes = get_unl_nodes()
        if not block.raund_1_node:
              dprint("Raund 1: in get candidate blocks\n")

 
              mynode.main_node.send_my_block(get_as_node_type(unl_nodes))
              block.raund_1_node = True
              block.save_block()
        candidate_class = GetCandidateBlocks()
        dprint("Raund 1 Conditions")
        dprint(len(candidate_class.candidate_blocks) > ((len(unl_nodes) * 80)/100))
        dprint((int(time.time()) - block.raund_1_starting_time) < block.raund_1_time)
        if len(candidate_class.candidate_blocks) > ((len(unl_nodes) * 80)/100):

         if not (int(time.time()) - block.raund_1_starting_time) < block.raund_1_time:
          temp_validating_list = []
          dprint("Raund 1: first ok")
          dprint(len(candidate_class.candidate_blocks))
          for candidate_block in candidate_class.candidate_blocks[:]:
              print(candidate_block)


              for other_block_tx in candidate_block["transaction"]:

                  tx_valid = 0

                  for my_txs in block.validating_list:
                      if other_block_tx.signature == my_txs.signature:
                          tx_valid += 1


                  if len(candidate_class.candidate_blocks) != 1:
                      dprint("Raund 1: Test tx")
                      for other_block in candidate_class.candidate_blocks[:]:
                         if candidate_block["signature"] != other_block["signature"]:
                            dprint("Raund 1: Test tx 2")
                            for other_block_txs in other_block["transaction"]:
                                if other_block_tx.signature == other_block_txs.signature:
                                    dprint("Raund 1: Test tx 3")
                                    tx_valid += 1
                  else:
                      tx_valid += 1


                  if tx_valid > (len(unl_nodes) / 2):
                      dprint("Raund 1: second ok")
                      already_in_ok = False
                      for alrady_tx  in temp_validating_list[:]:
                          
                          if other_block_tx.signature == alrady_tx.signature:
                              already_in_ok = True
                      if not already_in_ok:
                            dprint("Raund 1: third ok")
                            temp_validating_list.append(other_block_tx)




        
          newly_added_list = []
                
          for my_validating_list in block.validating_list[:]:
              ok = False
              for my_temp_validating_list in temp_validating_list[:]:
                  if my_validating_list.signature == my_temp_validating_list.signature:
                      ok = True
              block.validating_list.remove(my_validating_list) 
              if not ok:
                newly_added_list.append(my_validating_list)
                

                
          block.validating_list = temp_validating_list
        
          
          for each_newly in newly_added_list:
                CreateTransaction(block, each_newly.sequance_number, each_newly.signature, each_newly.fromUser, each_newly.toUser, each_newly.transaction_fee, each_newly.data, each_newly.amount, transaction_sender = None, transaction_time = each_newly.time)

          block.raund_1 = True

          block.raund_2_starting_time = int(time.time())

          



          ProccesstheTransaction(block)


          block.hash = CalculateHash(block)



          block.save_block()
        
                

         else:
            if not block.decrease_the_time == 3:
                block.decrease_the_time += 1
                block.increase_the_time = 0
                block.save_block()

        else:
            if not (int(time.time()) - block.raund_1_starting_time) < block.raund_1_time:
                if not block.increase_the_time == 3:
                    block.increase_the_time += 1
                    block.decrease_the_time = 0                
                    block.save_block()
