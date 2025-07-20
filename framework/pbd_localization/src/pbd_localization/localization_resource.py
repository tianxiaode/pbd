from typing import Dict, ClassVar,  Set,  Any
import copy
from pbd_core import DictHelper
from .exceptions import (
    EmptyResourceNameException,
    InvalidDefaultLanguageException,
)


class LocalizationResource:
    """
    本地化资源管理
    约定：
    1. 资源定义时可使用嵌套字典结构
    2. 内部自动转换为扁平化存储
    3. 查询路径格式：<资源名称>.<扁平键名>
    
    示例：
    class CommonResources(LocalizationResource):
        texts = {
            "en": {
                "common": {
                    "__public__": True, # 标记为公共资源
                    "button": {
                        "submit": "Submit",
                        "cancel": "Cancel"
                    },
                    "header": {
                        "welcome": "Welcome, {username}!"
                    }
                }
            },
            "zh-CN": {
                "common": {
                    "button": {
                        "submit": "提交",
                        "cancel": "取消"
                    },
                    "header": {
                        "welcome": "欢迎, {username}!"
                    }
                }
            }
        }
        
    
    查询示例：
    LocalizationResource.get("common.button.submit", "zh-CN")
    """
        
    _public_roots: ClassVar[Set[str]] = set()  # 基准语言公共根
    resources: ClassVar[Dict[str, Dict]] = {}
    _default_lang: ClassVar[str] = "en"
    _text_store: ClassVar[Dict[str, Dict]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._integrate_resources()

    @classmethod
    def _integrate_resources(cls):
        """整合资源并提取公共根标记"""
        for lang, lang_data in cls.resources.items():
            # 深度拷贝避免修改原始数据
            processed = DictHelper.deep_clone(lang_data)
            
            # 扫描第一层键
            for key in list(processed.keys()):
                if isinstance(processed[key], dict):
                    # 提取公共根标记
                    if processed[key].pop('__public__', False):
                        cls._public_roots.add(key)
                        
            # 合并到存储
            DictHelper.deep_merge(cls._text_store.setdefault(lang, {}), processed)

    @classmethod
    def get_full_pack(cls, lang: str) -> Dict:
        """获取完整嵌套结构"""
        return cls._text_store.get(lang, {})
    
    @classmethod
    def get_public_roots(cls) -> Set[str]:
        """获取公共根集合"""
        return cls._public_roots.copy()    

    @classmethod
    def get(cls, path: str, lang: str, default: Any = None) -> Any:
        """获取指定路径的本地化文本"""

        def find_in(lang: str):
            """多阶段查询函数"""
            # 阶段1：精确匹配
            if (val := DictHelper.find_by_path(cls._text_store.get(lang, {}), path)) is not None:
                return val
                
            # 阶段2：公共推导
            if '.' in path:
                _, _, suffix = path.partition('.')
                for root in cls._public_roots:
                    if (val := DictHelper.find_by_path(cls._text_store.get(lang, {}), f"{root}.{suffix}")) is not None:
                        return val
            return None
        

       # 主语言查询
        if (result := find_in(lang)) is not None:
            return result
            
        # 默认语言回退
        if lang != cls._default_lang:
            if (result := find_in(cls._default_lang)) is not None:
                return result
        
        return default

    @classmethod
    def get_default_lang(cls) -> str:
        """获取默认语言"""
        return LocalizationResource._default_lang

    @classmethod
    def set_default_lang(cls, lang: str):
        """设置默认语言"""
        if not isinstance(lang, str) or not lang:
            raise InvalidDefaultLanguageException()
        LocalizationResource._default_lang = lang

    @classmethod
    def get_all(cls, lang: str) -> Dict:
        """获取指定资源名称的本地化文本"""
        return copy.deepcopy(cls._text_store.get(lang, {}))



