from setuptools import setup
import os
import pathlib

setup(name='decentra_network_api',
version='0.9.0',
description="""This is API mode installer for Decentra Network Core""",
url='https://decentra-network.github.io/Decentra-Network/',
author='Decentra Network Developers',
author_email='atadogan06@gmail.com',
license='MPL-2.0',
install_requires=open(os.path.join((pathlib.Path(__file__) / ".." / ".." / "..").resolve(), 'requirements/api.txt' ), "r").read(),
python_requires=">=3.6",
zip_safe=False)
