#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from io import open

from setuptools import setup

setup(
    author="Decentra Network Developers",
    author_email="onur@decentranetwork.net",
    packages=["decentra_network"],
    name="decentra_network",
    version="0.41.0",
    url="https://github.com/Decentra-Network/Decentra-Network",
    description=
    "This is an open source decentralized application network. In this network, you can develop and publish decentralized applications.",
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
        "decentra-network",
        "githubcopilot",
        "blokzincir",
    ],
    long_description_content_type="text/markdown",
    long_description="".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dngui = decentra_network.gui.main:start",
            "dncli = decentra_network.cli.main:start",
            "dnapi = decentra_network.api.main:start",
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
