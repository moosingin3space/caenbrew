import contextlib
import os
import shutil
import subprocess
import tempfile

import click


def package(cls):
    """Mark a package as such.

    :param object cls: The class to mark as a package.
    """
    setattr(cls, "_is_package", True)
    return cls


def is_package(cls):
    """Determine whether the given class is a package.

    :param object cls: The class to check.
    :returns bool: Whether or not the class is a package.
    """
    return getattr(cls, "_is_package", False)


class BasePackage(object):
    """The base package installation class.

    The following variables should be defined by subclasses.

    :ivar str name: Required. The name of the package.
    :ivar list artifacts: Required. A list of files installed by the package.
        This is used to determine if the package is installed.
    :ivar str url: Required. The URL from which we can download the package.
    :ivar list configure_options: Optional. A list of arguments to pass to
        `configure`.
    """

    _ARCHIVE_DIR = "package_contents"
    """The directory to extract the archive into."""

    def __init__(self, config):
        """Initialize with the given configuration.

        :param dict config: The `caenbrew` configuration.
        """
        self._config = config

    @property
    def is_installed(self):
        """Determine whether this package is installed.

        :returns bool: Whether or not the package is installed.
        """
        if not self.artifacts:
            raise ValueError("Package {} must have non-empty "
                             "list of artifacts"
                             .format(self.name))

        def is_artifact_installed(artifact):
            artifact_path = os.path.join(self._config["prefix_dir"], artifact)
            return os.path.exists(artifact_path)
        return all(is_artifact_installed(i) for i in self.artifacts)

    @contextlib.contextmanager
    def prepare(self):
        """Set up the working directory to use for installation."""
        self._temp_dir = tempfile.mkdtemp()
        os.chdir(self._temp_dir)
        yield
        shutil.rmtree(self._temp_dir)

    def download(self):
        """Make a temporary directory and unpack the archive there."""
        archive_file = os.path.basename(self.url)

        self._cmd("curl", self.url,
                  "--output", archive_file,
                  title="Downloading {}".format(self.name))
        self._cmd("mkdir", "-p", self._ARCHIVE_DIR)
        self._cmd("tar",
                  "-xf", archive_file,
                  "-C", self._ARCHIVE_DIR,
                  "--strip-components", "1",
                  title="Extracting package")

    def install(self):
        """Configure, build, and install the package."""
        os.chdir(self._ARCHIVE_DIR)

        configure_options = getattr(self, "_configure_options", {})
        self._cmd("./configure",
                  "--prefix", self._config["prefix_dir"],
                  *configure_options,
                  title="Configuring package")

        self._cmd("make", title="Building package")
        self._cmd("make", "install", title="Installing package")

    def _cmd(self, *command, **kwargs):
        """Run the specified command in a subprocess.

        :param list command: The space-separated words in the command to run,
            as you would type it on the command line.
        :param str title: The title of this command.
        """
        title = kwargs.get("title")
        if title:
            click.echo("{}... ({})"
                       .format(click.style("==> " + title, bold=True),
                               " ".join(command)))

        if not self._config["verbose"]:
            with open(os.devnull, "w") as devnull:
                return_code = subprocess.call(command, stdout=devnull)
        else:
            return_code = subprocess.call(command)

        if return_code != 0:
            raise RuntimeError("Command '{}' failed".format(command[0]))
