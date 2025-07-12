import unittest
import asyncio
from unittest.mock import patch
from pbd_core import AsyncHelper
from typing import Any

class TestAsyncHelper(unittest.TestCase):
    def setUp(self):
        # 重置 _none_cache 以确保测试独立性
        AsyncHelper._none_cache = None
    
    def tearDown(self):
        # 清理
        AsyncHelper._none_cache = None
    
    def test_completed(self):
        """测试 completed() 方法"""
        # 第一次调用应该创建新的 Future
        fut1 = AsyncHelper.completed()
        self.assertIsInstance(fut1, asyncio.Future)
        self.assertTrue(fut1.done())
        self.assertIsNone(fut1.result())
        
        # 第二次调用应该返回缓存的 Future
        fut2 = AsyncHelper.completed()
        self.assertIs(fut1, fut2)
    
    def test_result(self):
        """测试 result() 方法"""
        test_value = "test result"
        fut = AsyncHelper.result(test_value)
        
        self.assertIsInstance(fut, asyncio.Future)
        self.assertTrue(fut.done())
        self.assertEqual(fut.result(), test_value)
    
    def test_error(self):
        """测试 error() 方法"""
        test_exception = ValueError("test error")
        fut = AsyncHelper.error(test_exception)
        
        self.assertIsInstance(fut, asyncio.Future)
        self.assertTrue(fut.done())
        with self.assertRaises(ValueError) as context:
            fut.result()
        self.assertEqual(str(context.exception), "test error")
    
    def test_run_sync_success(self):
        """测试 run_sync() 方法 - 成功情况"""
        def sync_func(a, b):
            return a + b
        
        fut = AsyncHelper.run_sync(sync_func, 2, 3)
        
        self.assertIsInstance(fut, asyncio.Future)
        self.assertTrue(fut.done())
        self.assertEqual(fut.result(), 5)
    
    def test_run_sync_failure(self):
        """测试 run_sync() 方法 - 失败情况"""
        def sync_func():
            raise ValueError("sync error")
        
        fut = AsyncHelper.run_sync(sync_func)
        
        self.assertIsInstance(fut, asyncio.Future)
        self.assertTrue(fut.done())
        with self.assertRaises(ValueError) as context:
            fut.result()
        self.assertEqual(str(context.exception), "sync error")
    
    @patch('asyncio.get_running_loop')
    def test_run_in_executor(self, mock_get_loop):
        """测试 run_in_executor() 方法"""
        # 创建一个真实的 Future 对象用于模拟返回值
        mock_future = asyncio.Future()
        mock_future.set_result(12)  # 3 * 4 = 12
        
        # 设置 mock 的返回值链
        mock_loop = unittest.mock.Mock()
        mock_loop.run_in_executor.return_value = mock_future
        mock_get_loop.return_value = mock_loop
        
        def sync_func(a, b):
            return a * b
        
        result = AsyncHelper.run_in_executor(sync_func, 3, 4)
        
        # 验证调用了 run_in_executor
        mock_loop.run_in_executor.assert_called_once_with(None, sync_func, 3, 4)
        
        # 验证返回的是 Future 对象
        self.assertIsInstance(result, asyncio.Future)
        
        # 验证结果值
        self.assertEqual(result.result(), 12)

    
    async def test_async_operations(self):
        """异步测试所有方法的协程行为"""
        # 测试 completed()
        fut1 = AsyncHelper.completed()
        self.assertIsNone(await fut1)
        
        # 测试 result()
        test_value = "async test"
        fut2 = AsyncHelper.result(test_value)
        self.assertEqual(await fut2, test_value)
        
        # 测试 error()
        test_ex = RuntimeError("async error")
        fut3 = AsyncHelper.error(test_ex)
        with self.assertRaises(RuntimeError):
            await fut3
        
        # 测试 run_sync()
        def sync_add(a, b):
            return a + b
        fut4 = AsyncHelper.run_sync(sync_add, 10, 20)
        self.assertEqual(await fut4, 30)
        
        # 测试 run_in_executor()
        def sync_mul(a, b):
            return a * b
        fut5 = AsyncHelper.run_in_executor(sync_mul, 5, 6)
        self.assertEqual(await fut5, 30)

if __name__ == '__main__':
    unittest.main()
