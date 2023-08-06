#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2022 PAL Robotics S.L. All rights reserved.

from pathlib import Path
from distutils.core import setup
import xml.etree.ElementTree as ET

NAME = "pal_app"

# get the version from ROS' package.xml
VERSION = ET.parse("package.xml").find("version").text

TPLS = [
    ("share/%s/%s" % (NAME, t.parent), [str(t)])
    for t in Path("tpl").rglob("*")
    if t.is_file()
]

setup(
    name=NAME,
    version=VERSION,
    license="Proprietary",
    description="A tool to create application controller skeletons for interactive robots",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    requires=["jinja2"],
    author="Séverin Lemaignan",
    author_email="severin.lemaignan@pal-robotics.com",
    scripts=["scripts/pal_app"],
    package_dir={"": "src"},
    packages=["pal_app"],
    data_files=TPLS + [("share/doc/pal_app", ["README.md", "LICENSE"])],
)
