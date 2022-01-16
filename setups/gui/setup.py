from setuptools import setup


setup(name='decentra_network_gui',
version='0.11.2',
description="""This is GUI mode installer for Decentra Network Core""",
url='https://decentra-network.github.io/Decentra-Network/',
author='Decentra Network Developers',
author_email='atadogan06@gmail.com',
license='MPL-2.0',
install_requires="""
Kivy==2.0.0
kivymd==0.104.1
kivymd_extensions.sweetalert==0.1.5
""",
python_requires=">=3.6",
zip_safe=False)
