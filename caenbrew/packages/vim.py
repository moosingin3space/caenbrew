from ._helpers import BasePackage, package


@package
class VimPackage(BasePackage):
    """VIM - Vi IMproved."""

    name = "vim"
    artifacts = ["bin/vim"]

    url = "ftp://ftp.vim.org/pub/vim/unix/vim-7.4.tar.bz2"
    configure_options = ["--enable-multibyte",
                         "--enable-python-interp=yes"]
