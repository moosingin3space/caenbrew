from ..packaging import AutotoolsPackage, package


@package
class HtopPackage(AutotoolsPackage):
    """htop - an interactive process viewer for UNIX."""

    name = "htop"
    homepage = "http://hisham.hm/htop"
    version = "2.0.1"
    artifacts = ["bin/htop"]

    url = "http://hisham.hm/htop/releases/2.0.1/htop-2.0.1.tar.gz"
