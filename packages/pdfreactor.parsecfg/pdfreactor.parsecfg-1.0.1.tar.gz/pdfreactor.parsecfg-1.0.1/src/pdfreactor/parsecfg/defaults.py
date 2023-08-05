"""
pdfreactor.parsecfg.defaults: default values
"""

# Python compatibility:
from __future__ import absolute_import

# PDFreactor (by RealObjects; Python integration by visaplan GmbH):
from pdfreactor.defaults import default_config as _cfg

default_config_text = """\
disableLinks = %(disableLinks)r
""" % _cfg
