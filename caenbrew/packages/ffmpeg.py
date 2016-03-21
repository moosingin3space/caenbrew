from .x264 import X264Package
from .yasm import YasmPackage

from ..packaging import AutotoolsPackage, package


@package
class FfmpegPackage(AutotoolsPackage):
    """Ffmpeg: record, convert and stream audio and video."""

    name = "ffmpeg"
    homepage = "https://www.ffmpeg.org/"
    version = "3.0"
    dependencies = [X264Package, YasmPackage]
    artifacts = ["bin/ffmpeg",
                 "bin/ffprobe",
                 "bin/ffserver",
                 "share/ffmpeg"]

    url = "http://ffmpeg.org/releases/ffmpeg-3.0.tar.bz2"
    configure_options = ["--enable-avresample",
                         "--enable-gpl",
                         "--enable-libx264",
                         "--enable-postproc",
                         "--enable-version3",
                         "--enable-x11grab",
                         "--enable-shared",
                         "--enable-pic"]

    def __init__(self, *args, **kwargs):
        """Help `ffmpg` detect `libx264` in `configure`."""
        super(FfmpegPackage, self).__init__(*args, **kwargs)
        prefix_dir = self._config["prefix_dir"]
        self.configure_options += ["--extra-ldflags=-L{}/lib"
                                   .format(prefix_dir),
                                   "--extra-cflags=-I{}/include"
                                   .format(prefix_dir)]
