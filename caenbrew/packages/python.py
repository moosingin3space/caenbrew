from ..packaging import package, SymlinkPackage


@package
class PythonPackage(SymlinkPackage):
    """Python is a general-purpose dynamic scripting language."""

    name = "python"
    homepage = "https://www.python.org/"
    version = "2.7.9"
    symlinks = {
        "/usr/um/python-2.7/bin/python": "bin/python",
    }
