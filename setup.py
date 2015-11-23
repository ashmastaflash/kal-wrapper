import os
from setuptools import setup

def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as f:
        filestring = f.read()
    return filestring

setup(name = "kalibrate",
      version = "1.0",
      author = "Ash Wilson",
      author_email = "ash.d.wilson@gmail.com",
      description = "A python wrapper for kalibrate-rtl",
      license = "BSD",
      keywords = "kalibrate kal rtl-sdr sdr",
      url = "https://github.com/ashmastaflash/kal-wrapper",
      packages = ["kalibrate", "test"],
      long_description = read("README.md"))
