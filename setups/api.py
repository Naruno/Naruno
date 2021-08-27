from setuptools import setup

setup(name='decentra_network_api',
version='0.8.0',
description="""This is API mode installer for Decentra Network Core""",
url='https://decentra-network.github.io/Decentra-Network/',
author='Decentra Network Developers',
author_email='atadogan06@gmail.com',
license='MPL-2.0',
install_requires=open("requirements/api.txt", "r").readlines(),
python_requires=">=3.6",
zip_safe=False)