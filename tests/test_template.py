""" Test the ansible-role Cookiecutter template.

A template project is created in a temporary directory, and the role's test
suite is run using molecule in a virtualenv environment.

"""
from json import load
from os import chdir
from os import environ
from os.path import pathsep
from pathlib import Path
from shlex import split
from subprocess import check_call
from tempfile import TemporaryDirectory
from venv import create

from cookiecutter.main import cookiecutter


def main():
    """ Execute the test.
    
    """
    def pymod(command: str):
        """ Run a Python module inside the virtual environment. """
        path = pathsep.join([str(venv.joinpath("bin")), environ["PATH"]])
        check_call(split(f"python -m {command:s}"), env={"PATH": path})
        return

    template = Path(__file__).resolve().parents[1]
    defaults = load(Path(template, "cookiecutter.json").open("rt"))
    with TemporaryDirectory() as tmpdir:
        chdir(tmpdir)
        cookiecutter(str(template), no_input=True)
        chdir(defaults["project_slug"])
        venv = Path(".venv")
        create(venv, with_pip=True)
        pymod("pip install -r molecule/requirements.txt")
        pymod("molecule test")
    return 0
    
    
# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
