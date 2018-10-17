import os
import re
from setuptools import setup

def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as f:
        filestring = f.read()
    return filestring

def get_version():
    raw_init_file = read("kalibrate/__init__.py")
    rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
    ver = rx_compiled.search(raw_init_file).group(1)
    return ver

def build_long_desc():
    return "\n".join([read(f) for f in ["README.rst", "CHANGELOG.rst"]])

setup(name = "kalibrate",
      version = get_version(),
      author = "Ash Wilson",
      author_email = "ash.d.wilson@gmail.com",
      description = "A python wrapper for kalibrate-rtl",
      license = "BSD",
      keywords = "kalibrate kal rtl-sdr sdr",
      url = "https://github.com/ashmastaflash/kal-wrapper",
      packages = ["kalibrate"],
      long_description = build_long_desc())
