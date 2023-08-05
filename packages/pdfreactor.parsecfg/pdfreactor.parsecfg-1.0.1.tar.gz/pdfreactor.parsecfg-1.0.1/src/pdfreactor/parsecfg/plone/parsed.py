"""
@@pdfreactor-config: parsed global settings
"""

# Python compatibility:
from __future__ import absolute_import

# Setup tools:
import pkg_resources

try:
    pkg_resources.get_distribution('pdfreactor.plone')
except pkg_resources.DistributionNotFound:
    HAVE_PDFREACTORPLONE = 0
else:
    HAVE_PDFREACTORPLONE = 1

# PDFreactor (by RealObjects; Python integration by visaplan GmbH):
from pdfreactor.api import PDFreactor

# Zope:
from Products.CMFCore.utils import getToolByName
from zope.interface import implements

# Local imports:
from pdfreactor.parsecfg.plone.interfaces import \
    IGetSettings  # ./interfaces.py
from pdfreactor.parsecfg.plone.interfaces import IPdfReactorConversionSettings

if HAVE_PDFREACTORPLONE:
    # PDFreactor (by RealObjects; Python integration by visaplan GmbH):
    from pdfreactor.plone.config import BaseSettingsView

    # ../../../../../pdfreactor.plone/src/pdfreactor/plone/config.py
else:
    # Zope:
    from Products.Five.browser import BrowserView as BaseSettingsView

# Local imports:
from ..convert import parse_configuration


class SettingsView(BaseSettingsView):

    implements(IGetSettings)  # usually IGetPdfReactorConversionSettings from
                              # pdfreactor.plone.interfaces

    def __call__(self, **kwargs):
        """
        Return the config dict or None

        In the standard case (without further arguments), the config dict is
        returned; if given by name, it is changed in-place, and None is
        returned.

        For the possible named arguments, see the parse_configuration function.

        NOTE: if you specify a config dict, this will serve as a set of
        defaults; any value might become overridden by the configured global
        setting (and the default cookies).

        """
        config_given = 'config' in kwargs
        if config_given:
            config = kwargs.pop('config')
        else:
            config = {}
        if HAVE_PDFREACTORPLONE:
            # will replace the 'cookies' value entirely:
            config.update(self.getZopeCookies())

        registry = getToolByName(self.context, 'portal_registry')
        dic = registry.forInterface(IPdfReactorConversionSettings)
        config_text = dic.config_text
        res = parse_configuration(config_text, config=config, **kwargs)
        if config_given:
            return res
        else:
            return config
