"""
    sphinxcontrib.gitloginfo
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Provide properties obtained from git log

    :copyright: Copyright 2020 by Martin Bless <martin.bless@mbless.de>
    :license: MIT, see LICENSE for details.
"""

import pbr.version

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa

__version__ = pbr.version.VersionInfo(
    'gitloginfo').version_string()


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    return {
        'version': __version__,
        'parallel_read_safe': True}
