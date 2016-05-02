""" Test the ansible-role Cookiecutter template.

A template project is created in a temporary directory, the application is
installed into a self-contained virtualenv environment, and the application
test suite is run.

"""
from contextlib import contextmanager
from os import chdir
from os import getcwd
from shlex import split
from shutil import rmtree
from subprocess import check_call
from tempfile import mkdtemp


def main():
    """ Execute the test.
    
    """
    @contextmanager
    def tmpdir():
        """ Enter a self-deleting temporary directory. """
        cwd = getcwd()
        tmp = mkdtemp()
        try:
            chdir(tmp)
            yield tmp
        finally:
            rmtree(tmp)
            chdir(cwd)
        return

    template = getcwd()
    with tmpdir():
        cookiecutter = "cookiecutter {:s} --no-input".format(template)
        check_call(split(cookiecutter))
        chdir("rolename")
        virtualenv = "virtualenv venv"
        check_call(split(virtualenv))
        install = "venv/bin/pip install --requirement=tests/requirements.txt"
        check_call(split(install))
        pytest = "venv/bin/python -m pytest --verbose tests"
        check_call(split(pytest))
    return 0
    
    
# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
