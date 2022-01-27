#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from setuptools import setup


setup(name='decentra_network_api',
version='0.12.0',
description="""This is API mode installer for Decentra Network Core""",
url='https://decentra-network.github.io/Decentra-Network/',
author='Decentra Network Developers',
author_email='atadogan06@gmail.com',
license='MPL-2.0',
install_requires="""
decentra-network==0.12.0
flask==2.0.0
waitress==2.0.0
""",
python_requires=">=3.6",
zip_safe=False)
