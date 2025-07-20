import unittest
from pbd_core import DictHelper

class TestDictHelper(unittest.TestCase):

    def test_flatten_happy_path(self):
        input_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        expected_output = {'a': 1, 'b.c': 2, 'b.d.e': 3}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_empty_dict(self):
        input_dict = {}
        expected_output = {}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_single_level_dict(self):
        input_dict = {'x': 10, 'y': 20, 'z': 30}
        expected_output = {'x': 10, 'y': 20, 'z': 30}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_nested_empty_dict(self):
        input_dict = {'a': {}, 'b': {'c': {}}}
        expected_output = {'a': {}, 'b.c': {}}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_with_different_separator(self):
        input_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        expected_output = {'a': 1, 'b_c': 2, 'b_d_e': 3}
        self.assertEqual(DictHelper.flatten(input_dict, sep='_'), expected_output)

    def test_flatten_with_parent_key(self):
        input_dict = {'a': 1, 'b': {'c': 2}}
        expected_output = {'root.a': 1, 'root.b.c': 2}
        self.assertEqual(DictHelper.flatten(input_dict, parent_key='root'), expected_output)

    def test_flatten_with_mixed_data_types(self):
        input_dict = {'a': 1, 'b': {'c': [2, 3], 'd': {'e': 'f'}}}
        expected_output = {'a': 1, 'b.c': [2, 3], 'b.d.e': 'f'}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_with_non_dict_value(self):
        input_dict = {'a': 1, 'b': 2}
        expected_output = {'a': 1, 'b': 2}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)
    
    def test_find_by_path_happy_path(self):
        input_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        self.assertEqual(DictHelper.find_by_path(input_dict, 'b.c'), 2)
        self.assertEqual(DictHelper.find_by_path(input_dict, 'b.d.e'), 3)
        self.assertEqual(DictHelper.find_by_path(input_dict, 'a'), 1)

    def test_find_by_path_nonexistent_path(self):
        input_dict = {'a': 1, 'b': {'c': 2}}
        self.assertIsNone(DictHelper.find_by_path(input_dict, 'a.b'))
        self.assertIsNone(DictHelper.find_by_path(input_dict, 'b.d'))
        self.assertIsNone(DictHelper.find_by_path(input_dict, 'c'))

    def test_find_by_path_empty_dict(self):
        self.assertIsNone(DictHelper.find_by_path({}, 'a'))
        self.assertIsNone(DictHelper.find_by_path({}, 'a.b.c'))

    def test_find_by_path_nested_dict(self):
        input_dict = {'level1': {'level2': {'level3': {'value': 42}}}}
        self.assertEqual(DictHelper.find_by_path(input_dict, 'level1.level2.level3.value'), 42)
        self.assertEqual(DictHelper.find_by_path(input_dict, 'level1.level2'), {'level3': {'value': 42}})

    def test_find_by_path_with_different_separator(self):
        input_dict = {'a': {'b': {'c': 10}}}
        self.assertEqual(DictHelper.find_by_path(input_dict, 'a/b', sep='/'), {'c': 10})
        self.assertEqual(DictHelper.find_by_path(input_dict, 'a/b/c', sep='/'), 10)

    def test_find_by_path_root_level(self):
        input_dict = {'root_value': 100}
        self.assertEqual(DictHelper.find_by_path(input_dict, 'root_value'), 100)

    def test_find_by_path_intermediate_dict(self):
        input_dict = {'a': {'b': {'c': 5}}}
        self.assertEqual(DictHelper.find_by_path(input_dict, 'a.b'), {'c': 5})

    def test_find_by_path_with_empty_string_path(self):
        input_dict = {'a': 1}
        self.assertIsNone(DictHelper.find_by_path(input_dict, ''))

    def test_deep_clone_happy_path(self):
        input_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}, '__public__': True}
        cloned = DictHelper.deep_clone(input_dict)
        self.assertEqual(cloned, {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}})
        self.assertIsNot(cloned, input_dict)
        self.assertIsNot(cloned['b'], input_dict['b'])

    def test_deep_clone_empty_dict(self):
        self.assertEqual(DictHelper.deep_clone({}), {})

    def test_deep_clone_with_nested_empty_dict(self):
        input_dict = {'a': {}, 'b': {'c': {}}}
        cloned = DictHelper.deep_clone(input_dict)
        self.assertEqual(cloned, {'a': {}, 'b': {'c': {}}})
        self.assertIsNot(cloned['a'], input_dict['a'])

    def test_deep_clone_with_non_dict_values(self):
        input_dict = {'a': [1, 2], 'b': "string", 'c': 123}
        cloned = DictHelper.deep_clone(input_dict)
        self.assertEqual(cloned, {'a': [1, 2], 'b': "string", 'c': 123})
        self.assertIs(cloned['a'], input_dict['a'])  # 列表是浅拷贝

    def test_deep_clone_with_multiple_public_flags(self):
        input_dict = {'__public__': True, 'a': {'__public__': False, 'b': 2}}
        cloned = DictHelper.deep_clone(input_dict)
        self.assertEqual(cloned, {'a': {'b': 2}})

    def test_deep_merge_happy_path(self):
        target = {'a': 1, 'b': {'c': 2}}
        source = {'b': {'d': 3}, 'e': 4}
        DictHelper.deep_merge(target, source)
        self.assertEqual(target, {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4})

    def test_deep_merge_empty_source(self):
        target = {'a': 1}
        source = {}
        DictHelper.deep_merge(target, source)
        self.assertEqual(target, {'a': 1})

    def test_deep_merge_empty_target(self):
        target = {}
        source = {'a': 1}
        DictHelper.deep_merge(target, source)
        self.assertEqual(target, {'a': 1})

    def test_deep_merge_overwrite_values(self):
        target = {'a': 1, 'b': {'c': 2}}
        source = {'a': 10, 'b': {'c': 20}}
        DictHelper.deep_merge(target, source)
        self.assertEqual(target, {'a': 10, 'b': {'c': 20}})

    def test_deep_merge_nested_dicts(self):
        target = {'level1': {'level2': {'a': 1}}}
        source = {'level1': {'level2': {'b': 2}, 'level3': 3}}
        DictHelper.deep_merge(target, source)
        expected = {'level1': {'level2': {'a': 1, 'b': 2}, 'level3': 3}}
        self.assertEqual(target, expected)

    def test_deep_merge_with_non_dict_values(self):
        target = {'a': {'b': 1}}
        source = {'a': 2}  # a从字典变为非字典值
        DictHelper.deep_merge(target, source)
        self.assertEqual(target, {'a': 2})


if __name__ == '__main__':
    unittest.main()
