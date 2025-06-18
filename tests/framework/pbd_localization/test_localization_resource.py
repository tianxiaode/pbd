import unittest
from unittest.mock import patch
from pbd_localization import LocalizationResource
from pbd_localization.exceptions import (
    ResourceNameDuplicateException,
    EmptyResourceNameException,
    InvalidTextsFormatException,
    InvalidLanguageFormatException,
    InvalidDefaultLanguageException,
)


class TestLocalizationResource(unittest.TestCase):
    def setUp(self):
        # 重置注册表以避免测试间干扰
        LocalizationResource._registry = {}
        LocalizationResource._public_registry = []
        LocalizationResource.texts = {}
        LocalizationResource._default_lang = "en"
        
        # 测试资源
        class TestResource(LocalizationResource):
            resource_name = "test_resource"
            texts = {
                'en': {'hello': 'Hello', 'goodbye': 'Goodbye'},
                'zh-CN': {'hello': '你好', 'goodbye': '再见'}
            }
        self.test_resource = TestResource()
        
        # 公共资源
        class PublicResource(LocalizationResource):
            resource_name = "public"
            texts = {
                'en': {'shared': 'Shared Text'},
                'zh-CN': {'shared': '共享文本'}
            }
            is_public = True
            
        # 私有资源
        class PrivateResource(LocalizationResource):
            resource_name = "private"
            texts = {
                'en': {'secret': 'Secret'},
                'zh-CN': {'secret': '秘密'}
            }
            is_public = False
            
    def test_get_default_lang(self):
        self.assertEqual(LocalizationResource.get_default_lang(), "en")

    def test_set_default_lang(self):
        LocalizationResource.set_default_lang("fr")
        self.assertEqual(LocalizationResource.get_default_lang(), "fr")

    def test_set_default_lang_invalid_value(self):
        with self.assertRaises(InvalidDefaultLanguageException):
            LocalizationResource.set_default_lang("")

        with self.assertRaises(InvalidDefaultLanguageException):
            LocalizationResource.set_default_lang(None)

    def test_get_with_valid_path(self):
        self.assertEqual(LocalizationResource.get("test_resource.hello", "en"), "Hello")
        self.assertEqual(LocalizationResource.get("test_resource.goodbye", "zh-CN"), "再见")

    def test_get_with_invalid_path(self):
        self.assertIsNone(LocalizationResource.get("test_resource.hello.world", "en"))
        self.assertIsNone(LocalizationResource.get("invalid_resource.hello", "en"))
    
    def test_get_with_default_value(self):
        self.assertEqual(LocalizationResource.get("test_resource.nonexistent", "en", "default_value"), "default_value")

    def test_get_with_fallback_to_default_lang(self):
        self.assertEqual(LocalizationResource.get("test_resource.hello", "nonexistent_lang"), "Hello")

    def test_get_from_public_resource(self):
        # 测试从公共资源获取
        self.assertEqual(LocalizationResource.get("public.shared", "en"), "Shared Text")
        self.assertEqual(LocalizationResource.get("public.shared", "zh-CN"), "共享文本")
        
        # 测试通过部分键名从公共资源获取
        self.assertEqual(LocalizationResource.get("test_resource.shared", "en"), "Shared Text")
        self.assertEqual(LocalizationResource.get("test_resource.shared", "zh-CN"), "共享文本")

    def test_not_get_from_private_resource(self):
        # 私有资源不应该通过部分键名获取
        self.assertIsNone(LocalizationResource.get("test_resource.secret", "en"))
        self.assertIsNone(LocalizationResource.get("test_resource.secret", "zh-CN"))
        
        # 只有完整路径才能获取私有资源
        self.assertEqual(LocalizationResource.get("private.secret", "en"), "Secret")
        self.assertEqual(LocalizationResource.get("private.secret", "zh-CN"), "秘密")

    def test_validate_resource_with_empty_resource_name(self):
        with self.assertRaises(EmptyResourceNameException):
            class InvalidResource(LocalizationResource):
                resource_name = ""
                texts = {}

    def test_validate_texts_with_invalid_format(self):
        with self.assertRaises(InvalidTextsFormatException):
            class InvalidTextsResource(LocalizationResource):
                resource_name = "invalid_texts"
                texts = "invalid_format"

        with self.assertRaises(InvalidLanguageFormatException):
            class InvalidTextsResource2(LocalizationResource):
                resource_name = "invalid_texts2"
                texts = {'en': 'invalid_format'}

        with self.assertRaises(InvalidLanguageFormatException):
            class InvalidTextsResource3(LocalizationResource):
                resource_name = "invalid_texts3"
                texts = {'en': {}, 'zh-CN': "invalid_format"}
    
    def test_duplicate_resource_name(self):
        with self.assertRaises(ResourceNameDuplicateException):
            class RepeatedResourceNameResource(LocalizationResource):
                resource_name = "test_resource"
                texts = {}

    def test_public_registry(self):
        self.assertIn("public", LocalizationResource._public_registry)
        self.assertNotIn("private", LocalizationResource._public_registry)

if __name__ == '__main__':
    unittest.main()
