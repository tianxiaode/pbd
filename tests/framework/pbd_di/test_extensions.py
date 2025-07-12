import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from pbd_di.extensions import lazy_resolve, IDependencyBase, Container

class TestService:
    pass

class TestExtension(unittest.IsolatedAsyncioTestCase):

    async def test_lazy_resolve_returns_coroutine_function(self):
        # 准备
        mock_container = MagicMock(spec=Container)
        mock_container.get = AsyncMock(return_value=TestService())
        
        # 使用 patch 替换 Container 的实例化
        with patch('pbd_di.extensions.Container', return_value=mock_container):
            # 执行
            resolver_func = lazy_resolve(None, TestService)
            
            # 验证返回的是可调用对象
            self.assertTrue(callable(resolver_func))
            
            # 调用返回的函数应该返回协程
            result = resolver_func()
            self.assertTrue(hasattr(result, '__await__'))
            
            # 执行协程应该调用容器的get方法
            resolved = await result
            mock_container.get.assert_called_once_with(TestService)
            self.assertIsInstance(resolved, TestService)

    def test_lazy_resolve_added_to_idependency_base(self):
        # 验证方法是否已添加到IDependencyBase
        self.assertTrue(hasattr(IDependencyBase, 'lazy_resolve'))
        self.assertTrue(callable(IDependencyBase.lazy_resolve))
