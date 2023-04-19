#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from io import open

from setuptools import setup

setup(
    author="Naruno Developers",
    author_email="onur.atakan.ulusoy@naruno.org",
    packages=["naruno"],
    name="naruno",
    version="0.57.1",
    url="https://github.com/Naruno/Naruno",
    description=
    "Naruno is a lightning-fast, secure, and scalable blockchain that is able to create transaction proofs and verification via raw data and timestamp. We remove the archive nodes and lazy web3 integrations. With Naruno everyone can get the proof (5-10MB) of their transactions via their nodes and after everyone can use in another node for verification the raw data and timestamp. Also you can integrate your web3 applications with 4 code lines (just python for now) via our remote app system.",
    keywords=[
        "python",
        "cryptography",
        "blockchain",
        "p2p",
        "python3",
        "cryptocurrency",
        "kivy",
        "coin",
        "copilot",
        "fba",
        "dapps",
        "p2p-network",
        "kivymd",
        "blokzinciri",
        "naruno",
        "githubcopilot",
        "blokzincir",
    ],
    long_description_content_type="text/markdown",
    long_description="".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "narunogui = naruno.gui.main:start",
            "narunocli = naruno.cli.main:start",
            "narunoapi = naruno.api.main:start",
        ],
    },
    license="MPL-2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)
