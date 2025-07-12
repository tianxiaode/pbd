from typing import Dict, Optional
from pbd_core import AsyncHelper
from .interfaces import ICultureStore , CultureInfo
from .default_culture import DefaultCulture

class DefaultCultureStore(ICultureStore):
    """
    默认的文化配置存储实现
    通过DefaultCulture来存储和管理文化配置
    未来可通过替换该类来实现其他的文化配置存储方式
    """
    
    def initialize(self):
        self._data = DefaultCulture()
    
    async def get_all(self)-> Dict[str, 'CultureInfo']:
        """获取所有文化配置"""
        return await AsyncHelper.result(self._data.get_all())
    
    async def get(self, code: str) -> Optional[CultureInfo]:
        """获取指定语言代码的文化配置"""
        return await AsyncHelper.result(self._data.get(code))
    
    async def add(self, data: CultureInfo):
        """添加或更新文化配置"""
        self._data.add(data)
        await AsyncHelper.completed()
    
    async def remove(self, code: str):
        """删除指定语言代码的文化配置"""
        self._data.remove(code)
        await AsyncHelper.completed()
    
    async def set_default(self, code: str):
        """设置默认文化配置"""
        self._data.set_default(code)
        await AsyncHelper.completed()
    
    async def get_default(self)-> Optional[CultureInfo]:
        """获取默认文化配置"""
        return await AsyncHelper.result(self._data.get_default())
    
    async def has(self)-> bool:
        """检查是否有文化配置"""
        return await AsyncHelper.result(bool(self._data.get_all()))
        