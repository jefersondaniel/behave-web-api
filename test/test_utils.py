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
