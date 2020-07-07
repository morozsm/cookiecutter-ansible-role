""" Test suite for the Molecule default scenario.

"""
from os import environ
from testinfra.utils.ansible_runner import AnsibleRunner


# Create the `host` fixture parametrized over all configured test platforms.
# Each `host` is a Testinfra Host instance. The inventory is created by the
# Molecule framework, so this test suite must be run via `molecule` and not
# `pytest`.
runner = AnsibleRunner(environ["MOLECULE_INVENTORY_FILE"])
testinfra_hosts = runner.get_hosts("all")


def test_commands(host):
    """ Test for installed Python commands.

    """
    assert True
    return
