import os
import sys
import subprocess
import pkg_resources


__package_name__ = "bget-ffmpeg-windows"
__version__ = pkg_resources.get_distribution(__package_name__).version
__bin__ = os.path.abspath(os.path.join(os.path.dirname(__file__), "bin"))


def __exec__(cmd):
    sys.exit(subprocess.call([os.path.join(__bin__, f"{cmd}.exe")] + sys.argv[1:]))

def ffmpeg():
    __exec__("ffmpeg")
