"""
    test_gitloginfo
    ~~~~~~~~~~~~~~~

    Test for gitloginfo extension.

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest


@pytest.mark.sphinx('html', testroot='basic')
def test_basic(app, status, warning):
    app.builder.build_all()
