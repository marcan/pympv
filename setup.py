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
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize

extensions=[
        Extension(
            "mpv",
            ["pympv/mpv.pyx"],
            libraries=['mpv']
        )
]

setup(
    name='pympv',
    version='0.1',
    packages=find_packages(),
    ext_modules = cythonize(extensions),
    setup_requires=[
        'Cython',
    ],
)
