"""Initialize the manager."""
import subprocess
import os
from pathlib import Path


class Manager():
    """Manager class."""

    def __init__(
            self, suite=None, mode=None, dev=False, beta=False, version=None):
        """Initialize the class."""
        self.beta = beta
        self.dev = dev
        self.exist = False
        self.mode = mode
        self.suite = suite
        self.suites = None
        self.version = version

    def is_installed(self):
        """Verify that hassbian-config is installed."""
        self.exist = bool(Path("/usr/local/bin/hassbian-config").is_file())
        return self.exist

    def get_suites(self):
        """Get a list of available suites."""
        self.suites = []
        for file in os.listdir("/opt/hassbian/suites"):
            if file.endswith(".sh"):
                self.suites.append(file[:-3])
        return self.suites

    def get_version(self):
        """Return the version of hassbian-config."""
        command = subprocess.Popen(
            ['hassbian-config', '--version'], stdout=subprocess.PIPE)
        out = command.communicate()
        version = str(out[0][:-1]).split("'")[1]
        return version

    def manage_suite(self):
        """Upgrade a suite with hassbian-config."""
        self.get_suites()
        if self.suite in self.suites:
            cmd = ['sudo', 'hassbian-config', self.mode]
            if self.dev:
                cmd.append(self.suite)
                cmd.append("--dev")
            elif self.beta:
                cmd.append(self.suite)
                cmd.append("--beta")
            else:
                if self.version:
                    cmd.append("{}={}".format(self.suite, self.version))
                else:
                    cmd.append(self.suite)
            cmd.append("--accept")
            subprocess.call(cmd)

    def os_upgrade(self):
        """Upgrade the base OS."""
        subprocess.call(
            ['sudo', 'hassbian-config', 'upgrade', 'hassbian',
             '--accept', '--dev'])

    def log(self):
        """Return log output."""
        command = subprocess.Popen(
            ['sudo', 'hassbian-config', 'log'], stdout=subprocess.PIPE)
        out = command.communicate()
        return out
