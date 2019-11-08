#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import re

import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))

README = os.path.join(ROOT, 'README.md')
VERSION = os.path.join(ROOT, 'hey/__init__.py')
REQUIREMENTS = os.path.join(ROOT, "requirements.txt")

with open(README, mode='rt', encoding='utf8') as fp:
    README = fp.read()

with open(VERSION, mode='rt', encoding='utf8') as fp:
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(REQUIREMENTS, mode='rt', encoding='utf-8') as fp:
    REQUIREMENTS = [line for line in fp.readlines() if line and '#' not in line]


def datafiles():
    return [('.', [
        'CHANGELOG.md',
        'README.md',
        'requirements.txt',
    ])]


if __name__ == "__main__":
    # allow setup.py to run from another directory
    os.chdir(ROOT)
    setuptools.setup(
        author='Helmut Konrad Fahrendholz',
        author_email='info@checkitweg.de',
        data_files=datafiles(),
        description='a lot of features',
        include_package_data=True,
        install_requires=REQUIREMENTS,
        long_description=README,
        name='hey',
        platforms='any',
        url='https://dev.package.checkitweg.de/hey',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.8',
        ],
        packages=[
            'detector',
            'detector.feature',
            'detector.parser',
            'groupme',
            'groupme.feature',
            'groupme.footer',
            'groupme.toc',
            'hey',
            'hey.fonts',
            'hey.textnavigator',
            'sections',
            'sections.feature',
            'words',
            'words.feature',
            'words.headlines',
            'words.loader',
            'words.text',
            'words.utils',
        ],
        entry_points={
            'console_scripts': [
                'detector = detector.cli:main',
                'groupme = groupme.cli:main',
                'hey = hey.cli:main',
                'sections = sections.cli:main',
                'words = words.cli:main',
            ],
        },
    )
