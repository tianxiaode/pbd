from abc import ABC, abstractmethod
from typing import Any, ClassVar
from pbd_di import ITransientDependency
from ..schema import SettingDefinition

class SettingValueProviderBase(ITransientDependency, ABC):
    """配置值提供者接口"""
    _register: ClassVar[list['SettingValueProviderBase']] = []  # 是否已注册
    name: ClassVar[str]
    priority: ClassVar[int] = 100  # 添加优先级属性，默认为100

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "name") or not isinstance(cls.name, str) or not cls.name:
            raise TypeError(
                f"子类 {cls.__name__} 必须定义 class 属性 `name`，且为非空字符串"
            )
            
        if not hasattr(cls, "priority") or not isinstance(cls.priority, int):
            raise TypeError(
                f"子类 {cls.__name__} 必须定义 class 属性 `priority`，且为整数"
            )
        
        SettingValueProviderBase._register.append(cls)

    @abstractmethod
    async def get(self, setting: SettingDefinition) -> Any:
        """获取配置值"""
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self, settings: list[SettingDefinition]) -> dict[str, Any]:
        """获取多个配置值"""
        raise NotImplementedError()
    
    @classmethod
    def get_providers(self) -> list['SettingValueProviderBase']:
        """获取所有配置值提供者的名称"""
        raise NotImplementedError()

