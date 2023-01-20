#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from setuptools import setup

setup(
    name="decentra_network_remote_app",
    version="0.41.0",
    description="""This is a tool for apps on Decentra Network""",
    url="https://docs.decentranetwork.net/",
    author="Decentra Network Developers",
    author_email="onur@decentranetwork.net",
    license="MPL-2.0",
    install_requires="""
requests==2.28.0
""",
    python_requires=">=3.8",
    zip_safe=False,
)
