from typing import ClassVar, Dict, Optional, Union, Any
from pydantic import BaseModel, field_validator
from .exceptions import SettingTypeError, SettingDuplicateError, SettingDefinitionError

class SettingDefinition(BaseModel):
    name: str   
    type: Union[str, type] 
    display_name: Optional[str] = None
    default_value: Optional[Any] = None
    description: Optional[str] = None
    is_visible_to_client: bool = True
    providers: Optional[list[str]] = None
    is_inherited: bool = False
    is_encrypted: bool = False
    key: Optional[str] = None

    @field_validator("type", mode='before')
    def normalize_type(cls, v):
        if isinstance(v, type):
            return v.__name__
        return v

class SettingSchema:
    settings: ClassVar[dict] = {}
    _registry: ClassVar[Dict[str, SettingDefinition]] = {}

    @staticmethod
    def _is_setting_definition(d: dict) -> bool:
        return 'type' in d  # 只要有type字段就认为是设置定义

    @classmethod
    def _create_setting_definition(cls, name: str, data: dict) -> SettingDefinition:
        return SettingDefinition(name=name, **data)

    @classmethod
    def _process_settings_dict(cls, settings_dict: dict, parent_key: str = ""):
        for key, value in settings_dict.items():
            current_key = f"{parent_key}.{key}" if parent_key else key
            
            if isinstance(value, dict):
                if cls._is_setting_definition(value):
                    setting = cls._create_setting_definition(key, value)
                    if current_key in cls._registry:
                        raise SettingDuplicateError(current_key)
                    setting.key = current_key
                    cls._registry[current_key] = setting
                else:
                    cls._process_settings_dict(value, current_key)
            else:
                raise SettingDefinitionError(f"不支持的设置类型: {type(value)}")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._process_settings_dict(cls.settings)

    @classmethod
    def get_all_settings(cls) -> Dict[str, SettingDefinition]:
        """获取所有已注册的设置(包括所有子类定义的设置)"""
        return dict(cls._registry)

    @classmethod
    def get_setting(cls, name: str) -> Optional[SettingDefinition]:
        """根据名称获取单个设置"""
        return cls._registry.get(name)

    @classmethod
    def get_settings_by_prefix(cls, prefix: str) -> Dict[str, SettingDefinition]:
        """根据前缀获取一组设置"""
        return {k: v for k, v in cls._registry.items() if k.startswith(prefix)}
