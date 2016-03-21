from .cmake import CmakePackage

from ..packaging import CmakeBuildPackage, package


@package
class YasmPackage(CmakeBuildPackage):
    """Yasm is a complete rewrite of the NASM assembler."""

    name = "yasm"
    homepage = "http://yasm.tortall.net/"
    version = "1.30"
    dependencies = [CmakePackage]
    artifacts = ["bin/yasm", "include/libyasm", "include/libyasm.h"]

    url = "http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz"
    configure_options = ["-DCMAKE_BUILD_TYPE=RELEASE"]
