#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import os
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from decentra_network.lib.config_system import get_config


def CleanUp_tests():

    os.chdir(get_config()["main_folder"])
    for the_file in os.listdir("db/"):
        if the_file.startswith("test_"):
            if os.path.isfile(f"db/{the_file}"):
                with contextlib.suppress(PermissionError):
                    os.remove(f"db/{the_file}")

    for the_file in os.listdir("apps/testing_app/"):
        if the_file.endswith(".tx"):
            if os.path.isfile(f"apps/testing_app/{the_file}"):
                with contextlib.suppress(PermissionError):
                    os.remove(f"apps/testing_app/{the_file}")

    for the_file in os.listdir(
            "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB/"):
        if the_file.endswith(".json") or the_file.endswith(".db"):

            os.remove(
                f"db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB/{the_file}"
            )

    for the_file in os.listdir("db/test_finished_main/"):
        if the_file.endswith(".json") or the_file.endswith(".db"):

            os.remove(f"db/test_finished_main/{the_file}")

    for the_file in os.listdir("db/test_proof_extracted/"):
        if the_file == "db":
            shutil.rmtree(f"db/test_proof_extracted/{the_file}")

    for the_file in os.listdir("db/extracted_proofs/"):
        if the_file != "README.md":
            shutil.rmtree(f"db/extracted_proofs/{the_file}")

    for the_file in os.listdir("db/test_finished_main_2/"):
        if the_file.endswith(".json") or the_file.endswith(".db"):

            os.remove(f"db/test_finished_main_2/{the_file}")

    for the_file in os.listdir("db/test_consensus_trigger_finished/"):
        if the_file.endswith(".json") or the_file.endswith(".db"):

            os.remove(f"db/test_consensus_trigger_finished/{the_file}")

    for the_file in os.listdir("db/connected_nodes_test_0/"):
        if the_file.endswith(".json") or the_file.endswith(".db"):

            os.remove(f"db/connected_nodes_test_0/{the_file}")
    for the_file in os.listdir("db/connected_nodes_test_1/"):
        if the_file.endswith(".json") or the_file.endswith(".db"):

            os.remove(f"db/connected_nodes_test_1/{the_file}")
    for the_file in os.listdir("db/connected_nodes_test_2/"):
        if the_file.endswith(".json") or the_file.endswith(".db"):

            os.remove(f"db/connected_nodes_test_2/{the_file}")

    for the_file in os.listdir("db/pending_transactions_test_1/"):
        if the_file.endswith(".json") or the_file.endswith(".db"):

            os.remove(f"db/pending_transactions_test_1/{the_file}")
    for the_file in os.listdir("db/pending_transactions_test_2/"):
        if the_file.endswith(".json") or the_file.endswith(".db"):

            os.remove(f"db/pending_transactions_test_2/{the_file}")


if __name__ == "__main__":
    CleanUp_tests()
