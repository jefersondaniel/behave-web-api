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
