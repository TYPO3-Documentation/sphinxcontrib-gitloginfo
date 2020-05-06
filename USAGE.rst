Usage
=====

Add `sphinxcontrib.gitloginfo` to the list of extensions to be loaded in
the `conf.py` file of your Sphinx project and optionally specify the desired
date and time format::

   extensions = ['sphinxcontrib.gitloginfo', …]
   html_last_updated_fmt = '%b %d, %Y %H:%M'  # = default


Make use of the provided variables in the Jinja2 html page templates. Choose
from:

• `{{ t3ctx.commit_hash }}`,
• `{{ t3ctx.last_modified }}`,
• `{{ t3ctx.last_modified_isoformat }}`,
• `{{ t3ctx.commit_url }}`.

