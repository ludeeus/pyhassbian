"""
A python module to interact with hassbian-config.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import subprocess
import os
from pathlib import Path


def get_is_installed():
    """Verify that hassbian-config is installed."""
    exist = bool(Path("/usr/local/bin/hassbian-config").is_file())
    return exist


def get_suites():
    """Get a list of available suites."""
    suites = []
    for file in os.listdir("/opt/hassbian/suites"):
        if file.endswith(".sh"):
            suites.append(file[:-3])
    return suites


def get_version():
    """Return the version of hassbian-config."""
    command = subprocess.Popen(['hassbian-config', '--version'],
                               stdout=subprocess.PIPE)
    out = command.communicate()[:-2]
    version = str(out[0][:-1]).split("'")[1]
    return version


def manage_suite(mode, suite, dev=False, beta=False, version=None):
    """Upgrade a suite with hassbian-config."""
    if suite in get_suites():
        if dev:
            subprocess.call(['sudo',
                             'hassbian-config',
                             mode,
                             suite,
                             '--accept',
                             '--dev'])
        elif beta:
            subprocess.call(['sudo',
                             'hassbian-config',
                             mode,
                             suite,
                             '--accept',
                             '--beta'])
        else:
            if version:
                subprocess.call(['sudo',
                                 'hassbian-config',
                                 mode,
                                 suite + '=' + str(version),
                                 '--accept'])
            else:
                subprocess.call(['sudo',
                                 'hassbian-config',
                                 mode,
                                 suite,
                                 '--accept'])


def os_upgrade():
    """Upgrade the base OS."""
    subprocess.call(['sudo',
                     'hassbian-config',
                     'upgrade',
                     'hassbian',
                     '--accept',
                     '--dev'])
