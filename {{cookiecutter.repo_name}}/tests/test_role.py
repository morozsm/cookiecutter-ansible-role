""" Test suite for the Ansible {{ cookiecutter.role_name }} role.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from os import chdir
from os import getcwd
from os.path import abspath
from os.path import basename
from os.path import dirname
from os.path import join
from shlex import split
from subprocess import check_call
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer
from threading import Thread
from tarfile import TarFile

import pytest


_ROLE = "{{ cookiecutter.role_name }}"


@pytest.fixture(scope="module")
def tmpdir(tmpdir_factory):
    """ Generate a test directory.

    """
    # Can't use the predefined tmpdir fixture because module scope is needed.
    return tmpdir_factory.mktemp("test_{:s}".format(_ROLE))


@pytest.fixture(scope="module")
def package(tmpdir):
    """ Package the role for installation by ansible-galaxy.

    """
    project_root = dirname(dirname(abspath(__file__)))
    package_path = join(tmpdir.strpath, "{:s}.tar.gz".format(_ROLE))
    with TarFile.open(package_path, "w:gz") as package:
        for name in "defaults", "handlers", "meta", "tasks", "tests", "vars":
            package.add(join(project_root, name), arcname=join(_ROLE, name))
    return package_path


@pytest.yield_fixture(scope="module")
def httpd(package):
    """ Return an HTTP URL to the packaged role.

    Files are served from the current working directory, so changing the
    directory while this fixture is being used will invalidate the URL.

    """
    # Yes, this is overkill for unit testing, but ansible-galaxy doesn't handle
    # local files very well.
    cwd = getcwd()
    chdir(dirname(package))
    httpd = TCPServer(("localhost", 0), SimpleHTTPRequestHandler)
    host, port = httpd.server_address
    thread = Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    yield "http://{:s}:{:d}/{:s}".format(host, port, basename(package))
    httpd.shutdown()
    chdir(cwd)
    return


@pytest.fixture(scope="module")
def install(tmpdir, httpd):
    """ Install the role and its dependencies for testing.

    """
    role_path = join(tmpdir.strpath, "roles")
    cmd = "ansible-galaxy install -p {:s} {:s}"
    check_call(split(cmd.format(role_path, httpd)))
    return role_path


def test_syntax(install):
    """ Test the role syntax.

    """
    cmd = "ansible-playbook --syntax-check playbook.yml"
    check_call(split(cmd), cwd=join(install, _ROLE, "tests"))
    return


# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main(__file__))
