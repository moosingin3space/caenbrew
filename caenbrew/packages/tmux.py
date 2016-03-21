from .libevent import LibeventPackage
from .ncurses import NcursesPackage

from ..packaging import ConfigurePackage, package


@package
class TmuxPackage(ConfigurePackage):
    """tmux is a terminal multiplexer."""

    name = "tmux"
    homepage = "https://tmux.github.io/"
    version = "2.1"
    dependencies = [LibeventPackage, NcursesPackage]

    artifacts = ["bin/tmux"]
    url = "https://github.com/tmux/tmux/releases/download/2.1/tmux-2.1.tar.gz"
