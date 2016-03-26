import os

from .nodejs import NodeJSPackage

from ..packaging import ArtifactPackage, package, TempDirMixin


@package
class AtomPackage(TempDirMixin, ArtifactPackage):
    """The Atom text editor."""

    name = "atom"
    homepage = "https://atom.io"
    version = "1.6.0"

    dependencies = [NodeJSPackage]

    artifacts = ["bin/atom", "bin/apm"]

    _GIT_REPO = "https://github.com/atom/atom"

    def download(self):
        """Download and extract the Atom text editor."""
        self._cmd("git", "clone", self._GIT_REPO)
        os.chdir("atom")
        self._cmd("git", "fetch", "-p")
        self._cmd("git", "checkout", "v1.6.0")

    def install(self):
        """Install the Atom text editor."""
        self._cmd("script/build")
        self._cmd("script/grunt", "install", "--install-dir", self.config["prefix_dir"])
