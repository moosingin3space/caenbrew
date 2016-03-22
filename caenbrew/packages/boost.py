from ..packaging import AutotoolsPackage, package


@package
class Boost(AutotoolsPackage):
    """Boost provides free peer-reviewed portable C++ source libraries."""

    name = "boost"
    homepage = "http://www.boost.org/"
    version = "1.59"
    artifacts = ["include/boost",
                 # There are a very large number of libraries installed which
                 # I don't want to list here, so I just picked a random one.
                 # (Get it?)
                 "lib/libboost_random.so"]

    url = "http://sourceforge.net/projects/boost/files/boost/1.59.0/boost_1_59_0.tar.bz2/download"  # noqa

    CONFIGURE_COMMAND = "./bootstrap.sh"
    BUILD_COMMAND = "./b2"
    INSTALL_COMMAND = "./b2"
