from ..packaging import package, AutotoolsPackage


@package
class NodeJSPackage(AutotoolsPackage):
    """Node.js is a JavaScript runtime."""

    name = "nodejs"
    homepage = "https://nodejs.org"
    version = "5.9.1"
    artifacts = ["bin/node", "bin/npm"]

    url = "https://nodejs.org/dist/v5.9.1/node-v5.9.1.tar.gz"
