# -*- coding: utf-8 -*-
"""`sphinxcontrib.gitloginfo` lives on `Github`_.

.. _github: https://github.com/TYPO3-Documentation/sphinxcontrib-gitloginfo
"""

import os
import re
import sys
from setuptools import find_packages, setup

PY3 = sys.version_info[0] >= 3
setup_requirements = []
test_requirements = []
extra_requirements = {
    'test': [
        'pytest',
        'flake8',
        'mypy',
    ],
}

if PY3:
    with open('README.rst', encoding='utf-8', errors='replace') as readme_file:
        readme = readme_file.read()
    with open('HISTORY.rst', encoding='utf-8', errors='replace') as history_file:
        history = history_file.read()
else:
    with open('README.rst') as readme_file:
        readme = readme_file.read().decode('utf-8', 'replace')
    with open('HISTORY.rst') as history_file:
        history = history_file.read().decode('utf-8', 'replace')

readme = re.compile('^.. BADGES_START.*^.. BADGES_END', re.M | re.S).sub('', readme)


def get_version():
    """Get version number of the package from version.py without importing core module."""
    package_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(package_dir, 'sphinxcontrib/gitloginfo/version.py')
    namespace = {}
    with open(version_file, 'rt') as f:
        exec(f.read(), namespace)
    return namespace['__version__']


setup(
    author='Martin Bless',
    author_email='martin.bless@mbless.de',
    description='Sphinx extension to provide data obtained from "git log" in the Sphinx page rendering context.',
    download_url='https://pypi.org/project/sphinxcontrib-gitloginfo/',
    license='MIT license',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    name='sphinxcontrib-gitloginfo',
    url='https://github.com/TYPO3-Documentation/sphinxcontrib-gitloginfo',
    version=get_version(),
    #
    entry_points={},
    extras_require=extra_requirements,
    include_package_data=True,
    namespace_packages=['sphinxcontrib'],
    packages=find_packages(exclude=['tests']),
    platforms='any',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    zip_safe=False,
    #
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Sphinx :: Extension',
        'Framework :: Sphinx',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Documentation',
    ],
)
