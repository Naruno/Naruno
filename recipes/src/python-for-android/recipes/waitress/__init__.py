#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pythonforandroid.recipe import PythonRecipe


class WaitressRecipe(PythonRecipe):
    version = "2.1.2"
    url = "https://files.pythonhosted.org/packages/72/83/c3de9799e2305898b02ea67bcd125ad06f271e2a82cc86fe66b7bf4e6f63/waitress-2.1.2.tar.gz"

    # call_hostpython_via_targetpython = True
    """If True, tries to install the module using the hostpython binary
    copied to the target (normally arm) python build dir. However, this
    will fail if the module tries to import e.g. _io.so. Set this to False
    to call hostpython from its own build dir, installing the module in
    the right place via arguments to setup.py. However, this may not set
    the environment correctly and so False is not the default."""

    # install_in_hostpython = False
    """If True, additionally installs the module in the hostpython build
    dir. This will make it available to other recipes if
    call_hostpython_via_targetpython is False.
    """

    # install_in_targetpython = True
    """If True, installs the module in the targetpython installation dir.
    This is almost always what you want to do."""

    # depends = []
    depends = []

    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = WaitressRecipe()
