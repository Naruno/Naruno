#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import os
import sys
from hashlib import sha256

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from naruno.config import SIGNS_PATH
from naruno.lib.config_system import get_config
from naruno.wallet.ellipticcurve.ecdsa import Ecdsa
from naruno.wallet.ellipticcurve.publicKey import PublicKey
from naruno.wallet.ellipticcurve.signature import Signature
from naruno.wallet.wallet_import import Address, wallet_import


def verify(path: str) -> bool:
    """
    Verifies the signature of the sign file.

    Args:
        path (str): Path of the sign file
    """
    sign_json = None
    os.chdir(get_config()["main_folder"])
    with contextlib.suppress(FileNotFoundError):
        with open(path, "r") as sign_file:
            sign_json = json.load(sign_file)

    if sign_json is None:
        return False


    result = (Ecdsa.verify(
        sign_json["data"],
        Signature.fromBase64(sign_json["signature"]),
        PublicKey.fromPem(sign_json["publickey"]),
    ), sign_json["data"], Address(sign_json["publickey"]))

    return result


if __name__ == "__main__":
    from naruno.lib.sign import sign

    print(verify(sign("Onur Atakan", "123")))
