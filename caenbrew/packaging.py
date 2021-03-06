import contextlib
import os
import subprocess
import tempfile

import click
import toposort


def package(cls):
    """Decorator to denote that a class is a package.

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


def calculate_dependencies(package_cls):
    """Get the dependencies for the package in installation order.

    :param BasePackage package_cls: The package class.
    :returns list: The packages in the order that they should be installed.
    """
    graph = {}

    def add_to_graph(cls):
        if cls in graph:
            return

        graph[cls] = set(cls.dependencies)
        for i in cls.dependencies:
            add_to_graph(i)

    add_to_graph(package_cls)
    return toposort.toposort_flatten(graph)


class BasePackage(object):
    """The base package installation class.

    The following variables should be defined by subclasses.

    :ivar str name: Required. The name of the package.
    :ivar str homepage: Required. The URL where the project homepage is.
    :ivar str version: Required. The version of the package.
    :ivar list dependencies: Optional. A list of `BasePackage`s which the
        package depends on. Defaults to the empty list.
    """

    dependencies = []
    """The packages that this one depends on."""

    def __init__(self, config):
        """Initialize with the given configuration.

        :param dict config: The `caenbrew` configuration.
        """
        self._config = config

        assert self.name
        assert self.homepage
        assert self.version

    @property
    def is_installed(self):
        """Whether or not this package is installed.

        Must be overridden by subclasses.
        """
        raise NotImplementedError()

    @contextlib.contextmanager
    def prepare(self):
        """Prepare to install the package.

        No-op; should be overridden by subclasses. This function should be a
        context manager.
        """
        yield

    def download(self):
        """Download the package source.

        No-op; should be overridden by subclasses.
        """
        pass

    def install(self):
        """Install the package.

        Must be overridden by subclasses.
        """
        raise NotImplementedError()

    def uninstall(self):
        """Uninstall the package.

        Must be overridden by subclasses.
        """
        raise NotImplementedError()

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


class ArtifactPackage(BasePackage):
    """A package that creates certain files (called "artifacts").

    Artifacts are used to determine whether or not a package is installed. If
    every listed artifact file exists, then the package is considered to be
    installed, and considered to not be installed otherwise.

    For a new package, the artifacts should be a good sample of representative
    installed files (such as one in `bin`, one in `include`, one in `lib`).

    The following variables should be defined by subclasses.

    :ivar list artifacts: Required. A list of files installed by the package.
        This is used to determine if the package is installed.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the package.

        Verify that the subclass has set the appropriate fields.
        """
        super(ArtifactPackage, self).__init__(*args, **kwargs)
        assert self.artifacts

    @property
    def is_installed(self):
        """Determine whether this package is installed.

        :returns bool: Whether or not the package is installed.
        """
        def is_artifact_installed(artifact):
            return os.path.exists(self._artifact_path(artifact))
        return all(is_artifact_installed(i) for i in self.artifacts)

    def uninstall(self):
        """Remove the package artifacts."""
        self._cmd("rm", "-r",
                  *[self._artifact_path(i) for i in self.artifacts],
                  title="Removing artifacts")

    def _artifact_path(self, artifact):
        """Get the path to a given artifact.

        :param str artifact: The artifact.
        :returns str: The full path to that artifact.
        """
        return os.path.join(self._config["prefix_dir"], artifact)


class TempDirMixin(object):
    """A mixin to implement moving to a temporary directory for preparation."""

    @contextlib.contextmanager
    def prepare(self):
        """Move to the temporary directory.

        Sets `self._temp_dir`.
        """
        self._temp_dir = tempfile.mkdtemp()
        os.chdir(self._temp_dir)
        yield
        self._cmd("rm", "-rf", self._temp_dir,
                  title="Cleaning up")


class ConfigureBuildInstallPackage(TempDirMixin, ArtifactPackage):
    """Install a package with a configure-build-install loop.

    By default, the `build_and_install` is set to use `make`. The `configure`
    function should be overridden by subclasses.

    The following variables should be defined by subclasses.

    :ivar str url: Required. The URL from which we can download the package.
    :ivar list configure_options: Optional. A list of arguments to pass to
        the configuration program.
    :ivar list make_options: Optional. A list of arguments to pass to `make`.
    """

    ARCHIVE_DIR = "package_contents"
    """The directory to extract the archive into."""

    BUILD_COMMAND = "make"
    """The executable to run to build and install the package."""

    INSTALL_COMMAND = "make"
    """The executable to run to build and install the package."""

    def download(self):
        """Make a temporary directory and unpack the archive there."""
        assert self.url
        archive_file = os.path.basename(self.url)

        self._cmd("curl", self.url,
                  "--output", archive_file,
                  # Follow redirects, such as those in Sourceforge links.
                  "--location",
                  title="Downloading {}".format(self.name))
        self._cmd("mkdir", "-p", self.ARCHIVE_DIR)
        self._cmd("tar",
                  "-xf", archive_file,
                  "-C", self.ARCHIVE_DIR,
                  "--strip-components", "1",
                  title="Extracting package")

    def install(self):
        """Configure, build, and install the package."""
        os.chdir(self.ARCHIVE_DIR)
        self.configure()
        self.build_and_install()

    def configure(self):
        """Configure the package."""
        raise NotImplementedError()

    def build_and_install(self):
        """Build and install the package with make."""
        make_options = getattr(self, "make_options", ["-j8"])
        self._cmd(self.BUILD_COMMAND,
                  *make_options,
                  title="Building package")
        self._cmd(self.INSTALL_COMMAND, "install",
                  title="Installing package")


class AutotoolsPackage(ConfigureBuildInstallPackage):
    """Install a package with autotools (marked by a `configure` script)."""

    CONFIGURE_COMMAND = "./configure"
    """The command to run to configure the package."""

    def configure(self):
        """Configure the package with the `configure` script."""
        configure_options = getattr(self, "configure_options", [])
        self._cmd(self.CONFIGURE_COMMAND,
                  # Some configure scripts don't like it if we separate the
                  # option from its value with a space (such as cmake's).
                  "--prefix={}".format(self._config["prefix_dir"]),
                  *configure_options,
                  title="Configuring package")


class CmakeBuildPackage(ConfigureBuildInstallPackage):
    """Install a package with Cmake.

    Named `CmakeBuildPackage` to avoid conflicts with the `CmakePackage`
    package.

    `cmake` must be declared as a dependency of the package.
    """

    BUILD_DIR = "build"
    """The directory to run `cmake` in."""

    def configure(self):
        """Configure, build, and install the package."""
        self._cmd("mkdir", "-p", self.BUILD_DIR)
        os.chdir(self.BUILD_DIR)

        configure_options = getattr(self, "configure_options", [])
        prefix_dir = self._config["prefix_dir"]
        self._cmd("cmake", "..",
                  "-DCMAKE_INSTALL_PREFIX={}".format(prefix_dir),
                  *configure_options,
                  title="Configuring package")


class SymlinkPackage(ArtifactPackage):
    """A package which can be installed by symlinking files into place.

    Subclasses may opt to omit the definition of `artifacts`. In this case, it
    is inferred from the symlinks.

    The following variables should be defined by subclasses.

    :ivar dict symlinks: A mapping from source files to destination files.
    """

    def __init__(self, *args, **kwargs):
        """Verify that there are symlinks for this package."""
        assert self.symlinks

        # Assume that the artifacts are the things we are symlinking to.
        if not getattr(self, "artifacts", None):
            self.artifacts = self.symlinks.values()

        super(SymlinkPackage, self).__init__(*args, **kwargs)

    def install(self):
        """Symlink all the files into place."""
        for source, dest in self.symlinks.iteritems():
            self._cmd("ln", "-s", source, self._artifact_path(dest),
                      title="Installing {}".format(os.path.basename(dest)))
