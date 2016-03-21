from ..packaging import ConfigurePackage, package


@package
class NcursesPackage(ConfigurePackage):
    """ncurses: An event notification library."""

    name = "ncurses"
    homepage = "http://invisible-island.net/ncurses/"
    version = "5.9"

    artifacts = ["include/ncurses", "lib/libncurses.a"]
    url = "ftp://invisible-island.net/ncurses/ncurses.tar.gz"
    configure_options = ["--enable-symlinks"]
