from pythonforandroid.recipe import PythonRecipe


class FlaskRecipe(PythonRecipe):
    version = "2.0.0"
    url = "https://files.pythonhosted.org/packages/37/6d/61637b8981e76a9256fade8ce7677e86a6edcd6d4525f459a6b9edbd96a4/Flask-2.0.0.tar.gz"

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

    # depends = ['Jinja2==3.1.2', 'MarkupSafe==2.1.1', 'Werkzeug==2.0.3', 'itsdangerous==2.1.2', 'click==8.1.3']
    depends = [
        "Jinja2",
        "MarkupSafe",
        "Werkzeug",
        "itsdangerous",
        "click",
    ]

    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = FlaskRecipe()
