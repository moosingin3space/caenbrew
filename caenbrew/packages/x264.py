from ..packaging import AutotoolsPackage, package


@package
class X264Package(AutotoolsPackage):
    """x264 is a library for encoding video streams into H.264/MPEG-4 AVC."""

    name = "x264"
    homepage = "http://www.videolan.org/developers/x264.html"
    version = "0.148.x"
    artifacts = ["bin/x264", "lib/libx264.a", "lib/libx264.so", "include/x264.h"]

    url = "ftp://ftp.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-20160321-2245-stable.tar.bz2"  # noqa
    configure_options = ["--enable-static",
                         "--enable-shared",
                         "--enable-pic"]
