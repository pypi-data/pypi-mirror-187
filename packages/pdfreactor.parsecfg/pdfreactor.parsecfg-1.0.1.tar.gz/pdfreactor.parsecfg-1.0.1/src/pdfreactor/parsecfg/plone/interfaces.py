"""
pdfreactor.plone.interfaces
"""

# Python compatibility:
from __future__ import absolute_import

from six import text_type as six_text_type

# Setup tools:
import pkg_resources

try:
    pkg_resources.get_distribution('pdfreactor.plone')
except pkg_resources.DistributionNotFound:
    HAVE_PDFREACTORPLONE = 0
else:
    HAVE_PDFREACTORPLONE = 1

# Zope:
from zope import schema

# Plone:
from plone.supermodel import model

# Local imports:
from pdfreactor.parsecfg.defaults import default_config_text

if HAVE_PDFREACTORPLONE:
    # PDFreactor (by RealObjects; Python integration by visaplan GmbH):
    from pdfreactor.plone.interfaces import \
        IGetPdfReactorConversionSettings as IGetSettingsBase
else:
    # Zope:
    from zope.interface import Interface as IGetSettingsBase


class IGetSettings(IGetSettingsBase):
    """
    Get a config dict for PDFreactor.convert (e.a.)
    """


class IPdfReactorConversionSettings(model.Schema):
    """
    PDFreactor conversion configuration
    """
    config_text = schema.Text(
        title=u"PDFreactor default conversion settings",
        default=six_text_type(default_config_text),
        required=False,
        description=(u"Default configuration for PDFreactor exports on this "
        u"site; parsed and converted to a config dictionary as expected e.g. "
        u"by the PDFreactor.convert method."
        ))
