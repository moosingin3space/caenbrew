from .cmake import CmakePackage
from .ffmpeg import FfmpegPackage

from ..packaging import CmakeBuildPackage, package


@package
class OpencvPackage(CmakeBuildPackage):
    """OpenCV: Open-source computer vision.

    THIS PACKAGE IS CURRENTLY BROKEN: It is in Caenbrew as a starting point but
    currently does not build. If you can fix it, please do so and open a pull
    request.

    The installation instructions for this package and most of its dependencies
    have been taken from this script:

    https://github.com/agiantwhale/caenhacks/blob/master/installcv.sh

    The fact that one needs to install so many dependencies is a sure sign that
    CAEN needs a package manager :)
    """

    name = "opencv"
    homepage = "http://opencv.org/"
    version = "2.4.12.3"
    artifacts = ["foo"]  # TODO

    # Note: Python and Numpy need to be dependencies for a fully-contained
    # installation of OpenCV. The latter has dependencies on some other
    # numerical libraries. I didn't bother to set up the `python-numpy`
    # package, but if CAEN upgrades in the future (and breaks the installed
    # Python and Numpy) it may be needed. Alternatively, just update the
    # configuration options.
    dependencies = [CmakePackage, FfmpegPackage]

    url = "https://github.com/Itseez/opencv/archive/2.4.12.3.tar.gz"
    configure_options = [
        "-DCMAKE_BUILD_TYPE=RELEASE",
        "-DCMAKE_CXX_COMPILER=/usr/bin/g++",
        "-DBUILD_NEW_PYTHON_SUPPORT=ON",
        "-DPYTHON2_EXECUTABLE=/usr/um/python-2.7/bin/python",
        "-DPYTHON2_INCLUDE=/usr/um/python-2.7/include/python2.7",
        "-DPYTHON2_LIBRARIES=/usr/um/python-2.7/lib/libpython2.7.so.1.0",
        "-DPYTHON2_PACKAGES_PATH=/usr/um/python-2.7/lib/python2.7/site-packages",  # noqa
        "-DPYTHON2_NUMPY_INCLUDE_DIRS=/usr/um/python-2.7/lib/python2.7/site-packages/numpy/core/include",  # noqa
        "-DWITH_IPP=OFF",
        "-DWITH_GTK=OFF",
        "-DWITH_V4L=OFF",
        "-DBUILD_ZLIB=TRUE",
        "-DBUILD_TIFF=TRUE",
        "-DBUILD_JASPER=TRUE",
        "-DBUILD_JPEG=TRUE",
        "-DBUILD_PNG=TRUE",
        "-DBUILD_OPENEXR=TRUE",
        "-DBUILD_TBB=TRUE",
    ]
