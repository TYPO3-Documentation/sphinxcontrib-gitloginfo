========================
sphinxcontrib-gitloginfo
========================

ATTENTION • work in progress • ATTENTION • WIP •
ATTENTION • work in progress • ATTENTION • WIP •
ATTENTION • work in progress • ATTENTION • WIP …


Overview
========

Sphinx-doc extension that provides info obtained from git log in the page rendering context.


Links
-----

- Source: https://github.com/TYPO3-Documentation/sphinxcontrib-gitloginfo
- Bugs: https://github.com/TYPO3-Documentation/sphinxcontrib-gitloginfo/issues


License
=======

MIT license


Details
=======

`confdir` is the path to the folder that contains the `conf.py` configuration
file.

This extension expects an optional `buildsettings.json` file in `confdir`.
It should at least contain a value for `t3docdir`, like
`{"t3docdir": "Documentation"}` or `{"t3docdir": "docs"}`.
`t3docdir` is the relative path from the project start to the docroot folder
inside the project. Sphinx is expecting such a folder with all the
documentation beneath (except includes and references). If the file is missing
`t3docdir = 'Documentation'` is used as default.

This extension expects a mandatory `gitloginfo.json` file in `confdir`. Without
this file the extension has no effect. The expected structure is::

   {
      "abspath_to_project": "/home/user/TYPO3.CMS.git/typo3/sysext/dashboard",
      "abspath_to_repo":    "/home/user/TYPO3.CMS.git",
      "filedata": {

         "typo3/sysext/project/Classes/Controller/AbstractController.php":
            [1587136226, "44ce57e72e3481224f745ca6db8f0f15372cc104"],

         "typo3/sysext/dashboard/Classes/ServiceProvider.php":
            [1586880838, "7b919798c8784ba3a3dd8cb82ab2d8a7e777878a"],

         "next/file/of/repository.ext":
            [utc-timestamp, "commit_hash"],

         "last/file/of/repository":
            [..., "..."]
      }
   }

Given this example the relative path from repo start to project start is
`typo3/sysext/dashboard`. "filedata" is a dictionary (associative array)
with filename and timestamp-commit_hash pairs as obtained from `git log`.
The timestamps are considered to represent UTC.

Date formatting

Sphinx knows a configuration option `html_last_updated_fmt`. This string is
used for date formatting. The default value is `'%b %d, %Y %H:%M'`.


Page rendering

If a page that is going to be rendered has a `sourcename` and a
`page_source_suffix` then a lookup in `filedata` is done to see whether we have
a `timestamp` and `commit_hash` for the file.

In this case we are trying to fetch or guess and assemble a
`commit_url_template` string.

Procedure:
First look for `commit_url_template`.
It should be the url to a commit with the actual commit hash replaces by
`%(commit_hash)s`. Examples:::

  https://github.com/user/repo/commit/%(commit_hash)s
  https://git.typo3.org/user/repo/commit/%(commit_hash)s
  https://bitbucket.org/user/repo/src/master/commits/%(commit_hash)s
  https://...gitlab.../user/repo/-/commit/%(commit_hash)s


If not given look for
`theme_project_repository`. If not given look for `theme_project_issues`. If
not given then we don't have a commit url and cannot link to that.

Page rendering context

If available these values will be added to the Jinja2 page rendering context::

   t3ctx['commit_hash']
   t3ctx['last_modified']
   t3ctx['last_modified_isoformat']
   t3ctx['commit_url']


Usage
=====

Add `sphinxcontrib.gitloginfo` to the list of extensions to be loaded in
the `conf.py` file of your Sphinx project and specify the desired date and time
format::

   extensions = ['sphinxcontrib.gitloginfo', …]
   html_last_updated_fmt = '%b %d, %Y %H:%M'


Use these values in the Jinja2 html templates:
`{{ t3ctx.commit_hash }}`,
`{{ t3ctx.last_modified }}`,
`{{ t3ctx.last_modified_isoformat }}`,
`{{ t3ctx.commit_url }}`.


Development
===========

The initial skeleton of this package was created with cookiecutter and
makes use of `pbr`::

   cookiecutter https://github.com/sphinx-contrib/cookiecutter

This version is kept in branch 'using-pbr'.

Install for local development:

#. Create a virtual Python environment
#. pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt
