from setuptools import setup

setup(name='decentra_network_api',
version='0.11.2',
description="""This is API mode installer for Decentra Network Core""",
url='https://decentra-network.github.io/Decentra-Network/',
author='Decentra Network Developers',
author_email='atadogan06@gmail.com',
license='MPL-2.0',
install_requires="""
flask==2.0.0
waitress==2.0.0
""",
python_requires=">=3.6",
zip_safe=False)
