""" Test suite for the {{ cookiecutter.role_name }} role.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from os.path import abspath
from os.path import dirname
from os.path import join
from shlex import split
from shutil import copytree
from subprocess import call
from subprocess import check_output

import pytest


@pytest.fixture
def install(tmpdir):
    """ Install the role in a temporary working directory.

    """
    pathobj = tmpdir.join("{{ cookiecutter.role_name }}")
    dirs = "defaults", "handlers", "meta", "tasks", "tests", "vars"
    root = dirname(dirname(abspath(__file__)))
    for name in dirs:
        copytree(join(root, name), join(pathobj.strpath, name))
    return pathobj.strpath


def test_role(install):
    """ Test the role syntax.

    """
    ansible = "ansible-playbook --syntax-check playbook.yml"
    assert 0 == call(split(ansible), cwd=join(install, "tests"))
    return


# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main(__file__))
