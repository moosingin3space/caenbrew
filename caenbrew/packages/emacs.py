from ._helpers import BasePackage, package


@package
class EmacsPackage(BasePackage):
    """emacs - GNU project Emacs."""

    name = "emacs"
    artifacts = ["bin/emacs"]

    url = "http://ftp.wayne.edu/gnu/emacs/emacs-24.5.tar.xz"
    configure_options = ["--with-xpm=no",
                         "--with-gif=no",
                         "--with-tiff=no"]
