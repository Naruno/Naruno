#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
import sys
from hashlib import sha256

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from decentra_network.config import SIGNS_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.wallet.ellipticcurve.ecdsa import Ecdsa
from decentra_network.wallet.ellipticcurve.privateKey import PrivateKey
from decentra_network.wallet.wallet_import import wallet_import


def sign(data: str, password: str) -> str:
    """
    Signs the data with the private key of the user.

    Args:
        data (str): Data to be signed
        password (str): Password of the current wallet
    """

    my_private_key = wallet_import(-1, 1, password)
    signature = Ecdsa.sign(
        data,
        PrivateKey.fromPem(my_private_key),
    ).toBase64()

    sign_json = {
        "data": data,
        "signature": signature,
        "publickey": wallet_import(-1, 0),
    }

    sign_path = os.path.join(
        SIGNS_PATH, sha256((signature).encode("utf-8")).hexdigest() + ".dnsign"
    )

    os.chdir(get_config()["main_folder"])
    with open(sign_path, "w") as sign_file:
        json.dump(sign_json, sign_file)

    return sign_path


if __name__ == "__main__":
    print(sign("Ali Eren", "123"))
