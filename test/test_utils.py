import unittest
from behave_web_api import utils


class UtilsTest(unittest.TestCase):
    def test_is_comparing_values_with_matched_regex(self):
        error = None

        try:
            utils.compare_values(
                {
                    'hi': '%.+%'
                },
                {
                    'hi': 'Hello'
                }
            )
        except AssertionError as e:
            error = e

        self.assertEqual(None, error)

    def test_is_comparing_values_with_non_matched_regex(self):
        error = None

        try:
            utils.compare_values(
                {
                    'hi': 'dsa'
                },
                {
                    'hi': 'Hello'
                }
            )
        except AssertionError as e:
            error = e

        self.assertEqual(
            'Expected \'Hello\' to equal \'dsa\' at path hi',
            error.args[0]
        )

    def test_is_comparing_dicts(self):
        error = None

        try:
            utils.compare_values(
                {
                    'a': {
                        'b': {
                            'c': [3]
                        }
                    }
                },
                {
                    'a': {
                        'b': {
                            'c': [4]
                        }
                    }
                }
            )
        except AssertionError as e:
            error = e

        self.assertEqual(
            'Expected 4 to equal 3 at path a.b.c.0',
            error.args[0]
        )

    def test_is_comparing_contents_with_matched_regex(self):
        error = None

        try:
            utils.compare_contents(
                r'%my name is \w+%',
                'Hi my name is Bob Bob'
            )
        except AssertionError as e:
            error = e

        self.assertEqual(None, error)

    def test_is_comparing_contents_with_non_matched_regex(self):
        error = None

        try:
            utils.compare_contents(
                r'%my name is not \w+%',
                'Hi my name is Bob Bob'
            )
        except AssertionError as e:
            error = e

        self.assertEqual(
            'Expected response to contain regex \'%my name is not \\w+%\'',
            error.args[0]
        )

    def test_is_comparing_contents_with_matched_string(self):
        error = None

        try:
            utils.compare_contents(
                'my name is',
                'Hi my name is Bob Bob'
            )
        except AssertionError as e:
            error = e

        self.assertEqual(None, error)

    def test_is_comparing_contents_with_non_matched_string(self):
        error = None

        try:
            utils.compare_contents(
                'my name is not',
                'Hi my name is Bob Bob'
            )
        except AssertionError as e:
            error = e

        self.assertEqual(
            'Expected response to contain text \'my name is not\'',
            error.args[0]
        )

    def test_path_for_multiple_list_items(self):
        """Test that path is correctly computed for multiple items in a list"""
        error = None

        try:
            utils.compare_values(
                [1, 2, 3],
                [1, 2, 999]
            )
        except AssertionError as e:
            error = e

        # The error should be at index 2, not some accumulated path
        self.assertEqual(
            'Expected 999 to equal 3 at path 2',
            error.args[0]
        )

    def test_path_for_multiple_dict_keys(self):
        """Test that path is correctly computed for multiple keys in a dict"""
        errors = []

        # Test first key
        try:
            utils.compare_values(
                {'a': 1, 'b': 2, 'c': 3},
                {'a': 999, 'b': 2, 'c': 3}
            )
        except AssertionError as e:
            errors.append(e.args[0])

        # Test second key
        try:
            utils.compare_values(
                {'a': 1, 'b': 2, 'c': 3},
                {'a': 1, 'b': 999, 'c': 3}
            )
        except AssertionError as e:
            errors.append(e.args[0])

        # Test third key
        try:
            utils.compare_values(
                {'a': 1, 'b': 2, 'c': 3},
                {'a': 1, 'b': 2, 'c': 999}
            )
        except AssertionError as e:
            errors.append(e.args[0])

        self.assertEqual('Expected 999 to equal 1 at path a', errors[0])
        self.assertEqual('Expected 999 to equal 2 at path b', errors[1])
        self.assertEqual('Expected 999 to equal 3 at path c', errors[2])

    def test_path_for_nested_list_with_multiple_errors(self):
        """Test that path is correctly computed in nested structures"""
        error = None

        try:
            utils.compare_values(
                {'items': [{'id': 1}, {'id': 2}, {'id': 3}]},
                {'items': [{'id': 1}, {'id': 2}, {'id': 999}]}
            )
        except AssertionError as e:
            error = e

        # Should be items.2.id, not something like items.0.1.2.id
        self.assertEqual(
            'Expected 999 to equal 3 at path items.2.id',
            error.args[0]
        )

    def test_path_for_list_in_nested_dict(self):
        """Test path computation for lists inside nested dicts"""
        error = None

        try:
            utils.compare_values(
                {'data': {'users': ['alice', 'bob', 'charlie']}},
                {'data': {'users': ['alice', 'bob', 'eve']}}
            )
        except AssertionError as e:
            error = e

        self.assertEqual(
            'Expected \'eve\' to equal \'charlie\' at path data.users.2',
            error.args[0]
        )

    def test_get_nested_value_simple_key(self):
        """Test get_nested_value with simple dictionary key"""
        obj = {'name': 'Alice'}
        result = utils.get_nested_value(obj, 'name')
        self.assertEqual('Alice', result)

    def test_get_nested_value_nested_keys(self):
        """Test get_nested_value with nested dictionary keys"""
        obj = {'user': {'name': 'Alice', 'age': 30}}
        result = utils.get_nested_value(obj, 'user.name')
        self.assertEqual('Alice', result)

    def test_get_nested_value_list_index(self):
        """Test get_nested_value with list index"""
        obj = {'items': [1, 2, 3]}
        result = utils.get_nested_value(obj, 'items.1')
        self.assertEqual(2, result)

    def test_get_nested_value_mixed_path(self):
        """Test get_nested_value with mixed dict and list path"""
        obj = {
            'data': {
                'users': [
                    {'name': 'Alice', 'age': 30},
                    {'name': 'Bob', 'age': 25}
                ]
            }
        }
        result = utils.get_nested_value(obj, 'data.users.1.name')
        self.assertEqual('Bob', result)

    def test_get_nested_value_nonexistent_key(self):
        """Test get_nested_value with nonexistent key"""
        obj = {'name': 'Alice'}
        result = utils.get_nested_value(obj, 'age')
        self.assertIsNone(result)

    def test_get_nested_value_out_of_bounds_index(self):
        """Test get_nested_value with out of bounds list index"""
        obj = {'items': [1, 2, 3]}
        result = utils.get_nested_value(obj, 'items.10')
        self.assertIsNone(result)

    def test_get_nested_value_invalid_path_type(self):
        """Test get_nested_value with invalid path (non-dict/list)"""
        obj = {'value': 'string'}
        result = utils.get_nested_value(obj, 'value.nested')
        self.assertIsNone(result)

    def test_object_matches_exact_match(self):
        """Test object_matches with exact match"""
        actual = {'a': 1, 'b': 2}
        expected = {'a': 1, 'b': 2}
        self.assertTrue(utils.object_matches(actual, expected))

    def test_object_matches_partial_match(self):
        """Test object_matches with partial match (actual has extra fields)"""
        actual = {'a': 1, 'b': 2, 'c': 3}
        expected = {'a': 1, 'b': 2}
        self.assertTrue(utils.object_matches(actual, expected))

    def test_object_matches_missing_field(self):
        """Test object_matches when actual is missing expected field"""
        actual = {'a': 1}
        expected = {'a': 1, 'b': 2}
        self.assertFalse(utils.object_matches(actual, expected))

    def test_object_matches_wrong_value(self):
        """Test object_matches when value doesn't match"""
        actual = {'a': 1, 'b': 999}
        expected = {'a': 1, 'b': 2}
        self.assertFalse(utils.object_matches(actual, expected))

    def test_object_matches_nested_objects(self):
        """Test object_matches with nested objects"""
        actual = {
            'user': {
                'name': 'Alice',
                'address': {
                    'city': 'NYC',
                    'country': 'USA',
                    'zip': '10001'
                },
                'age': 30
            }
        }
        expected = {
            'user': {
                'name': 'Alice',
                'address': {
                    'country': 'USA'
                }
            }
        }
        self.assertTrue(utils.object_matches(actual, expected))

    def test_object_matches_nested_objects_mismatch(self):
        """Test object_matches with nested objects that don't match"""
        actual = {
            'user': {
                'address': {
                    'country': 'USA'
                }
            }
        }
        expected = {
            'user': {
                'address': {
                    'country': 'Canada'
                }
            }
        }
        self.assertFalse(utils.object_matches(actual, expected))

    def test_object_matches_with_lists(self):
        """Test object_matches with lists (exact match required for lists)"""
        actual = {'tags': ['python', 'javascript']}
        expected = {'tags': ['python', 'javascript']}
        self.assertTrue(utils.object_matches(actual, expected))

    def test_object_matches_with_different_list_length(self):
        """Test object_matches with lists of different lengths"""
        actual = {'tags': ['python', 'javascript', 'java']}
        expected = {'tags': ['python', 'javascript']}
        self.assertFalse(utils.object_matches(actual, expected))

    def test_object_matches_type_mismatch(self):
        """Test object_matches when types don't match"""
        actual = {'value': 'string'}
        expected = {'value': 123}
        self.assertFalse(utils.object_matches(actual, expected))

    def test_object_matches_primitives(self):
        """Test object_matches with primitive values"""
        self.assertTrue(utils.object_matches(42, 42))
        self.assertTrue(utils.object_matches('hello', 'hello'))
        self.assertFalse(utils.object_matches(42, 43))

    def test_get_nested_value_with_none_intermediate(self):
        """Test get_nested_value when intermediate value is None"""
        obj = {'user': None}
        result = utils.get_nested_value(obj, 'user.name')
        self.assertIsNone(result)

    def test_object_matches_with_none_values(self):
        """Test object_matches with None values"""
        self.assertTrue(utils.object_matches(None, None))
        self.assertFalse(utils.object_matches({'a': None}, {'a': 1}))
        self.assertTrue(utils.object_matches({'a': None, 'b': 2}, {'a': None}))
