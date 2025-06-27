# interfaces.py
from abc import ABC, abstractmethod
from typing import Any, Type, Protocol, runtime_checkable
from ..schema import SettingDefinition

class ISettingValueProvider(Protocol):
    name: str
    priority: int
    
    @abstractmethod
    async def get(self, setting: SettingDefinition) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, settings: list[SettingDefinition]) -> dict[str, Any]:
        raise NotImplementedError

class IProviderRegistry(Protocol):
    @abstractmethod
    def register(self, provider: Type[ISettingValueProvider]) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_provider_classes(self) -> list[Type[ISettingValueProvider]]:
        raise NotImplementedError
    
    @abstractmethod
    def get_sorted_provider_classes(self) -> list[Type[ISettingValueProvider]]:
        raise NotImplementedError

class IProvider(IProviderRegistry, ISettingValueProvider, Protocol):
    """组合接口（不需要额外方法）"""
    pass