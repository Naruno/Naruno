#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import time

from lib.mixlib import dprint

from node.unl import get_as_node_type
from node.myownp2pn import mynode

from blockchain.block.candidate_blocks import get_candidate_block
from blockchain.block.calculate_hash import CalculateHash

from transactions.process_the_transaction import ProccesstheTransaction

def consensus_round_1(block):
        if not block.raund_1_node:
              dprint("Raund 1: in get candidate blocks\n")

 
              mynode.main_node.send_my_block(get_as_node_type(block.total_validators))
              block.raund_1_node = True
              block.save_block()
        candidate_class = get_candidate_block()
        dprint("Raund 1 Conditions")
        dprint(len(candidate_class.candidate_blocks) > ((len(block.total_validators) * 80)/100))
        dprint((int(time.time()) - block.raund_1_starting_time) < block.raund_1_time)
        if len(candidate_class.candidate_blocks) > ((len(block.total_validators) * 80)/100):
         if len(candidate_class.candidate_blocks) == len(block.total_validators) or not (int(time.time()) - block.raund_1_starting_time) < block.raund_1_time:
          temp_validating_list = []
          dprint("Raund 1: first ok")
          dprint(len(candidate_class.candidate_blocks))
          for candidate_block in candidate_class.candidate_blocks[:]:


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


                  if tx_valid > (len(block.total_validators) / 2):
                      dprint("Raund 1: second ok")
                      already_in_ok = False
                      for alrady_tx  in temp_validating_list[:]:
                          
                          if other_block_tx.signature == alrady_tx.signature:
                              already_in_ok = True
                      if not already_in_ok:
                            dprint("Raund 1: third ok")
                            temp_validating_list.append(other_block_tx)





          for my_validating_list in block.validating_list[:]:
              ok = False
              for my_temp_validating_list in temp_validating_list[:]:
                  if my_validating_list.signature == my_temp_validating_list.signature:
                      ok = True
              block.validating_list.remove(my_validating_list) 
              if not ok:
                block.createTrans(my_validating_list.sequance_number, my_validating_list.signature, my_validating_list.fromUser, my_validating_list.toUser, my_validating_list.transaction_fee, my_validating_list.data, my_validating_list.amount, transaction_sender = None)
                

                
          block.validating_list = temp_validating_list      


          block.raund_1 = True

          block.raund_2_starting_time = int(time.time())

          



          ProccesstheTransaction(block)


          block.hash = CalculateHash(block)



          block.save_block()
