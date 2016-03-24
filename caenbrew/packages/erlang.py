from .ncurses import NcursesPackage
from .wxwidgets import WxWidgetsPackage

from ..packaging import AutotoolsPackage, package


@package
class ErlangPackage(AutotoolsPackage):
    """erlang/otp - build massively scalable soft real-time systems."""

    name = "erlang"
    homepage = "http://www.erlang.org"
    version = "18.3"
    dependencies = [NcursesPackage, WxWidgetsPackage]

    url = "http://www.erlang.org/download/otp_src_18.3.tar.gz"
    artifacts = ["bin/erl", "lib/erlang"]
