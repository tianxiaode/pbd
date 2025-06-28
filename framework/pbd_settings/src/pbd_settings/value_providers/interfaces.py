# interfaces.py
from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict, List, Type
from pbd_di import ITransientDependency
from ..schema import SettingDefinition

class ISettingValueProvider(ITransientDependency, ABC):
    """配置值提供者接口"""
    name: ClassVar[str]  # 必须定义

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, 'name'):
            ISettingValueProvider._providers[cls.name] = cls

    @abstractmethod
    async def get(self, setting: SettingDefinition) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, settings: List[SettingDefinition]) -> Dict[str, Any]:
        raise NotImplementedError

# class IProviderRegistry(ABC):
#     """提供者注册表接口（自动注册子类）"""
#     _providers: ClassVar[Dict[str, Type[ISettingValueProvider]]] = {}

#     def __init_subclass__(cls, **kwargs):
#         super().__init_subclass__(**kwargs)
#         if hasattr(cls, 'name'):
#             IProviderRegistry._providers[cls.name] = cls

#     @classmethod
#     def get_providers(cls) -> List[Type[ISettingValueProvider]]:
#         """获取所有提供者类（按优先级排序）"""
#         return sorted(
#             cls._providers.values(),
#             key=lambda x: x.priority
#         )
    
# # manager.py
# from typing import List
# from pbd_di import IServiceProvider
# from .interfaces import IProviderRegistry, ISettingValueProvider

# class SettingProviderManager:
#     def __init__(self, service_provider: IServiceProvider):
#         self.service_provider = service_provider

#     async def get_all_providers(self) -> List[ISettingValueProvider]:
#         """获取所有提供者实例（按优先级排序）"""
#         return [
#             await self.service_provider.get(provider_cls)
#             for provider_cls in IProviderRegistry.get_providers()
#         ]

#     async def resolve_setting(self, setting_def) -> Any:
#         """按优先级解析配置值"""
#         for provider in await self.get_all_providers():
#             if (value := await provider.get(setting_def)) is not None:
#                 return value
#         return None