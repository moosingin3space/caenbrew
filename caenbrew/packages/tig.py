from .git import GitPackage
from .ncurses import NcursesPackage

from ..packaging import AutotoolsPackage, package


@package
class TigPackage(AutotoolsPackage):
    """Tig: Text-mode Interface for Git."""

    name = "tig"
    homepage = "http://jonas.nitro.dk/tig/"
    version = "2.1.1"
    dependencies = [GitPackage, NcursesPackage]
    artifacts = ["bin/tig"]

    url = "http://jonas.nitro.dk/tig/releases/tig-2.1.1.tar.gz"
