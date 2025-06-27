from pbd_core import PbdModuleBase
from pbd_security import SecurityModule
from .value_providers import DefaultValueSettingValueProvider, GlobalSettingsValueProvider, JsonSettingsValueProvider, UserSettingsValueProvider

class SettingsModule(PbdModuleBase):
     _deps=[SecurityModule]

