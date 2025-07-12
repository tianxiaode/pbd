from typing import Any, Type, Callable, Coroutine
from .interfaces import IDependencyBase, TDependency
from .container import Container

def lazy_resolve(self, service_type: Type[TDependency]) -> Callable[[], Coroutine[Any, Any, TDependency]]:
    """延迟解析依赖项（由DI扩展提供）"""
    container = Container()  # 获取当前容器实例
    
    async def resolver() -> TDependency:
        return await container.get(service_type)
    
    return resolver

# 将方法动态添加到IDependencyBase
IDependencyBase.lazy_resolve = lazy_resolve