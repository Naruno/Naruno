from pythonforandroid.recipe import PythonRecipe
import os
from os.path import basename, dirname, exists, isdir, isfile, join, realpath, split
import glob
from shutil import rmtree
from six import with_metaclass

import hashlib
from re import match

import sh
import shutil
import fnmatch
import urllib.request
from urllib.request import urlretrieve
from os import listdir, unlink, environ, mkdir, curdir, walk
from sys import stdout
import time
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from pythonforandroid.logger import (logger, info, warning, debug, shprint, info_main)
from pythonforandroid.util import (current_directory, ensure_dir,
                                   BuildInterruptingException)
from pythonforandroid.util import load_source as import_recipe


url_opener = urllib.request.build_opener()
url_orig_headers = url_opener.addheaders
urllib.request.install_opener(url_opener)

class DecentraNetworkRecipe(PythonRecipe):
    version = '0.25.0'
    url = 'https://files.pythonhosted.org/packages/b5/2d/6255510a4881ed28b0da6b035f1823fbe14488bc2857a6c4bce8d0bf2dde/decentra_network-0.25.0.tar.gz'

    #call_hostpython_via_targetpython = True
    '''If True, tries to install the module using the hostpython binary
    copied to the target (normally arm) python build dir. However, this
    will fail if the module tries to import e.g. _io.so. Set this to False
    to call hostpython from its own build dir, installing the module in
    the right place via arguments to setup.py. However, this may not set
    the environment correctly and so False is not the default.'''

    #install_in_hostpython = False
    '''If True, additionally installs the module in the hostpython build
    dir. This will make it available to other recipes if
    call_hostpython_via_targetpython is False.
    '''

    #install_in_targetpython = True
    '''If True, installs the module in the targetpython installation dir.
    This is almost always what you want to do.'''

    # depends = []
    depends = ["setuptools"]

    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def download_file(self, url, target, cwd=None):
        """
        (internal) Download an ``url`` to a ``target``.
        """
        backup = os.getcwd()
        the_directory = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
        os.chdir(the_directory)
        debug((f"\n\n{os.getcwd()}\n{self.version}\n{target}\n\n"))
        os.system("python3 setup.py sdist")
        time.sleep(5)
        os.system(f"cp dist/decentra_network-{self.version}.tar.gz {backup}/{target}")
        os.chdir(backup) 



recipe = DecentraNetworkRecipe()
