from ..packaging import AutotoolsPackage, package


@package
class FishPackage(AutotoolsPackage):
    """fish is a smart and user-friendly command line shell."""

    name = "fish"
    homepage = "https://fishshell.com/"
    version = "2.2.0"
    artifacts = ["bin/fish"]

    url = "https://fishshell.com/files/2.2.0/fish-2.2.0.tar.gz"
