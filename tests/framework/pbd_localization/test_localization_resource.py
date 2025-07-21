import unittest
from unittest.mock import patch
from pbd_localization import LocalizationResource
from pbd_localization.exceptions import (
    NoResourceException,
    InvalidResourceFormatException,
    InvalidDefaultLanguageException,
)


class TestLocalizationResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 重置类变量
        LocalizationResource._public_roots = set()
        LocalizationResource.resources = {}
        LocalizationResource._text_store = {}
        LocalizationResource._default_lang = "en"

    def setUp(self):
        """每个测试用例前重置状态"""
        # 重置类变量
        self.setUpClass()

    def test_invalid_resource_format(self):
        """测试资源格式不正确时抛出异常"""
        with self.assertRaises(InvalidResourceFormatException):
            class InvalidResource(LocalizationResource):
                resources = "invalid"


    def test_valid_resources_integration(self):
        """测试资源整合功能"""
        class TestResource(LocalizationResource):
            resources = {
                "en": {
                    "common": {
                        "_public": True,
                        "button": {
                            "submit": "Submit",
                            "cancel": "Cancel"
                        }
                    },
                    "app": {
                        "title": "My App"
                    }
                },
                "zh-CN": {
                    "common": {
                        "button": {
                            "submit": "提交",
                            "cancel": "取消"
                        }
                    }
                }
            }

        # 验证公共根
        self.assertEqual(LocalizationResource.get_public_roots(), {"common"})
        
        # 验证资源存储
        self.assertEqual(LocalizationResource._text_store["en"]["common"]["button"]["submit"], "Submit")
        self.assertEqual(LocalizationResource._text_store["zh-CN"]["common"]["button"]["submit"], "提交")
        self.assertEqual(LocalizationResource._text_store["en"]["app"]["title"], "My App")

    def test_get_method(self):
        """测试get方法"""
        class TestResource(LocalizationResource):
            resources = {
                "en": {
                    "common": {
                        "_public": True,
                        "button": {
                            "submit": "Submit",
                            "cancel": "Cancel"
                        }
                    },
                    "app": {
                        "title": "My App"
                    }
                },
                "zh-CN": {
                    "common": {
                        "button": {
                            "submit": "提交",
                            "cancel": "取消"
                        }
                    }
                }
            }

        # 测试精确匹配
        self.assertEqual(LocalizationResource.get("common.button.submit", "en"), "Submit")
        self.assertEqual(LocalizationResource.get("common.button.submit", "zh-CN"), "提交")
        
        # 测试默认语言回退
        self.assertEqual(LocalizationResource.get("app.title", "zh-CN"), "My App")
        
        # 测试不存在的路径
        self.assertIsNone(LocalizationResource.get("not.exist", "en"))
        self.assertEqual(LocalizationResource.get("not.exist", "en", "default"), "default")

    def test_get_full_pack(self):
        """测试获取完整资源包"""
        class TestResource(LocalizationResource):
            resources = {
                "en": {
                    "common": {
                        "button": {
                            "submit": "Submit"
                        }
                    }
                }
            }

        result = LocalizationResource.get_full_pack("en")
        self.assertEqual(result["common"]["button"]["submit"], "Submit")

    def test_get_all(self):
        """测试获取指定语言所有资源"""
        class TestResource(LocalizationResource):
            resources = {
                "en": {
                    "common": {
                        "button": {
                            "submit": "Submit"
                        }
                    }
                }
            }

        result = LocalizationResource.get_all("en")
        self.assertEqual(result["common"]["button"]["submit"], "Submit")

    def test_default_language(self):
        """测试默认语言设置"""
        # 测试获取默认语言
        self.assertEqual(LocalizationResource.get_default_lang(), "en")
        
        # 测试设置默认语言
        LocalizationResource.set_default_lang("zh-CN")
        self.assertEqual(LocalizationResource.get_default_lang(), "zh-CN")
        
        # 测试设置无效默认语言
        with self.assertRaises(InvalidDefaultLanguageException):
            LocalizationResource.set_default_lang("")
        with self.assertRaises(InvalidDefaultLanguageException):
            LocalizationResource.set_default_lang(None)

    def test_nested_resources(self):
        """测试嵌套资源结构"""
        class NestedResource(LocalizationResource):
            resources = {
                "en": {
                    "level1": {
                        "level2": {
                            "level3": {
                                "value": "deep_value"
                            }
                        }
                    }
                }
            }

        self.assertEqual(LocalizationResource.get("level1.level2.level3.value", "en"), "deep_value")

    def test_public_root_derivation(self):
        """测试公共根推导功能"""
        class PublicResource(LocalizationResource):
            resources = {
                "en": {
                    "common": {
                        "_public": True,
                        "actions": {
                            "save": "Save",
                            "load": "Load"
                        }
                    },
                    "app": {
                        "actions": {
                            "exit": "Exit"
                        }
                    }
                },
                "zh-CN": {
                    "common": {
                        "actions": {
                            "save": "保存",
                            "load": "加载"
                        }
                    }
                }
            }

        # 测试公共根推导
        self.assertEqual(LocalizationResource.get("user.actions.save", "en"), "Save")
        self.assertEqual(LocalizationResource.get("user.actions.save", "zh-CN"), "保存")
        


if __name__ == "__main__":
    unittest.main()
