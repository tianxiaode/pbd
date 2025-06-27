
from typing import Any
from .base import SettingValueProviderBase, SettingDefinition
from ..interfaces import ISettingStore

class GlobalSettingsValueProvider(SettingValueProviderBase):
    _name = 'G'
    _deps = [ISettingStore]

    def initialize(self):
        """初始化"""
        self._store = self.get_dependency(ISettingStore)

    async def get(self, setting: SettingDefinition) -> Any:
        """获取配置值"""
        return await self._store.get(setting, self._name)

    async def get_all(self, settings: list[SettingDefinition]) -> dict[str, Any]:
        """获取所有配置值"""
        return await self._store.get_all(settings, self._name)