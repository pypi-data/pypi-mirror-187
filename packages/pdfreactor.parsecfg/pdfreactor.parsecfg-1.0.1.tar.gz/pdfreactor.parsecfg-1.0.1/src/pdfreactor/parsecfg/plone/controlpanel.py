from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from pdfreactor.parsecfg.plone.interfaces import IPdfReactorConversionSettings
from plone.z3cform import layout
from z3c.form import form

class ConversionControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IPdfReactorConversionSettings

ConversionControlPanelView = layout.wrap_form(ConversionControlPanelForm, ControlPanelFormWrapper)
ConversionControlPanelView.label = u"PDFreactor Conversion settings"
