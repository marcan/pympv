#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from glob import glob
from os.path import join

from setuptools import Extension, find_packages, setup

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
    extension_src = "mpv.pyx"
except ImportError:
    USE_CYTHON = False
    extension_src = "mpv.c"

extra_data = {}
extensions = [Extension("mpv", [extension_src], libraries=["mpv"])]

if set(["setup.py", "--version", "-V"]) >= set(sys.argv):
    extensions = []

if set(["bdist_wheel", "--plat-name", "win_amd64"]) <= set(sys.argv):
    extra_data["data_files"] = [
        ("Scripts", ["mpv.dll"]),
        ("libs", ["mpv.lib"]),
        ("include", glob("mpv/*")),
    ]
    extensions = [
        Extension(
            "mpv",
            [extension_src],
            libraries=["mpv"],
            library_dirs=[os.curdir],
            include_dirs=[join(os.curdir, "mpv")],
        )
    ]

if USE_CYTHON:
    extensions = cythonize(extensions, force=True)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pympv",
    version="0.7.0",
    description="Python bindings for the libmpv library",
    # This is supposed to be reST. Cheating by using a common subset of
    # reST and Markdown...
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Andre D",
    author_email="andre@andred.ca",
    maintainer="Hector Martin",
    maintainer_email="marcan@marcan.st",
    url="https://github.com/marcan/pympv",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Cython",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    ext_modules=extensions,
    **extra_data
)
