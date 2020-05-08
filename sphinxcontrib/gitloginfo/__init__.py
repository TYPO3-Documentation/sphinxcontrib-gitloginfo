"""
    sphinxcontrib.gitloginfo
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Provide properties obtained from git log

    :copyright: Copyright 2020 by Martin Bless <martin.bless@mbless.de>
    :license: MIT, see LICENSE for details.
"""

import datetime
import io
import json
import sys

from os.path import exists as ospe, join as ospj
from sphinx.util import i18n, logging
from sphinxcontrib.gitloginfo.version import __version__

log = logging.getLogger(__name__)
PY2 = sys.version_info[0] == 2
wd = workdata = {}

if PY2:

    class UtcTzinfo(datetime.tzinfo):
        """UTC"""

        ZERO = datetime.timedelta(0)

        def utcoffset(self, dt):
            return self.ZERO

        def tzname(self, dt):
            return "UTC"

        def dst(self, dt):
            return self.ZERO

    utc_tzinfo = UtcTzinfo()
else:
    utc_tzinfo = datetime.timezone.utc


def _html_page_context(app, pagename, templatename, context, doctree):
    if 'sourcename' in context and 'page_source_suffix' in context:
        pass
    else:
        return
    pagename_as_repofile = ospj(wd['project_offset'],
                                wd['t3docdir'],
                                pagename + context['page_source_suffix'])
    v = wd['filedata'].get(pagename_as_repofile, (None, None))
    timestamp = v[0]
    commit_hash = v[1]
    if timestamp is None:
        log.info("[%s] %s :: not found" % (__name__, pagename_as_repofile))
        return
    else:
        log.info("[%s] %s :: found" % (__name__, pagename_as_repofile))
    last_modified_dt = datetime.datetime.fromtimestamp(timestamp, utc_tzinfo)
    last_modified = i18n.format_date(wd['html_last_updated_fmt'],
                                     date=last_modified_dt,
                                     language=app.config.language)
    # Try to assemble or guess a commit url
    commit_url_template = context.get('theme_project_commit_url')
    if not commit_url_template:
        # Maybe we can deduce the url needed
        repo_url = (context.get('theme_project_repository') or
                    context.get('theme_project_issues'))
        if repo_url:
            # Github
            if repo_url.startswith('https://github.com/'):
                if repo_url.endswith('/issues'):
                    repo_url = repo_url[:-7]
                elif repo_url.endswith('.git'):
                    repo_url = repo_url[:-4]
                commit_url_template = repo_url + '/commit/%(commit_hash)s'
            # git.typo3.org
            elif repo_url.startswith('https://git.typo3.org/'):
                if repo_url.endswith('/issues'):
                    repo_url = repo_url[:-7]
                commit_url_template = repo_url + '/commit/%(commit_hash)s'
            # bitbucket
            elif repo_url.startswith('https://bitbucket.org/'):
                if repo_url.endswith('/src/master/'):
                    repo_url = repo_url[:-12]
                commit_url_template = repo_url + '/commits/%(commit_hash)s'
            # gitlab
            elif "gitlab" in repo_url[:repo_url[8:].find('/')+8]:
                if repo_url.endswith('/-/issues'):
                    repo_url = repo_url[:-9]
                commit_url_template = repo_url + '/-/commit/%(commit_hash)s'

    t3ctx = context['t3ctx'] = context.get('t3ctx', {})
    t3ctx['commit_hash'] = commit_hash
    t3ctx['last_modified'] = last_modified
    t3ctx['last_modified_isoformat'] = last_modified_dt.isoformat()
    if commit_url_template:
        t3ctx['commit_url'] = commit_url_template % {'commit_hash': commit_hash}


def _config_inited(app, config):
    v = getattr(app.config, 'html_last_updated_fmt', None)
    wd['html_last_updated_fmt'] = v if v else '%b %d, %Y %H:%M'


def setup(app):
    """Sphinx extension entry point."""
    app.require_sphinx('1.8')  # For "config-inited" event

    buildsettings_jsonfile = ospj(app.confdir, 'buildsettings.json')
    if ospe(buildsettings_jsonfile):
        # just collect knowledge
        wd['buildsettings_jsonfile'] = buildsettings_jsonfile
        with io.open(buildsettings_jsonfile, 'r', encoding='utf-8') as f1:
            wd['buildsettings'] = json.load(f1)
        log.info("[%s] app.confdir/buildsettings.json :: found" % (__name__,))
    else:
        log.info("[%s] app.confdir/buildsettings.json :: not found" % (__name__,))

    gitloginfo_jsonfile = ospj(app.confdir, 'gitloginfo.json')
    if ospe(gitloginfo_jsonfile):
        # just collect knowledge
        wd['gitloginfo_jsonfile'] = gitloginfo_jsonfile
        with io.open(gitloginfo_jsonfile, 'r', encoding='utf-8') as f1:
            wd['gitloginfo'] = json.load(f1)
        log.info("[%s] app.confdir/gitloginfo.json :: found" % (__name__,))

        wd['filedata'] = wd['gitloginfo'].get('filedata', {})
        wd['project_offset'] = (wd['gitloginfo']['abspath_to_project']
                                [len(wd['gitloginfo']['abspath_to_repo']):]
                                .strip('/'))
        wd['t3docdir'] = wd.get('buildsettings', {}).get('t3docdir',
                                                         'Documentation')
    else:
        log.info("[%s] app.confdir/gitloginfo.json :: not found" % (__name__,))
    if wd.get('filedata'):
        # only connect if there is something to do
        app.connect('html-page-context', _html_page_context)
        app.connect('config-inited', _config_inited)
        log.info("[%s] filedata found" % (__name__,))
    else:
        log.info("[%s] filedata not found" % (__name__,))

    return {
        'version': __version__,
        'parallel_read_safe': True,
    }
