from ..packaging import ConfigureBuildInstallPackage, package


@package
class CppcheckPackage(ConfigureBuildInstallPackage):
    """Cppcheck is a static analysis tool for C/C++ code."""

    name = "cppcheck"
    homepage = "http://cppcheck.sourceforge.net/"
    version = "1.72"
    artifacts = ["bin/cppcheck"]

    url = "http://downloads.sourceforge.net/project/cppcheck/cppcheck/1.72/cppcheck-1.72.tar.bz2"  # noqa

    def __init__(self, *args, **kwargs):
        """Set `make` to use a `PREFIX`."""
        super(CppcheckPackage, self).__init__(*args, **kwargs)
        self.make_options = ["PREFIX={}".format(self._config["prefix_dir"])]

    def configure(self):
        """No-op."""
