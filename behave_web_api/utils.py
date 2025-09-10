import os
import re
import requests
from functools import wraps

string_type = str


def make_url(context, endingpoint):
    BASE_URL = dereference_variables(context, '$BASE_URL')
    if 'http' not in BASE_URL:
        BASE_URL = 'http://{0}'.format(BASE_URL)

    return '{0}{1}'.format(BASE_URL, endingpoint)


def dereference_variables(context, value):
    variables = context.variables\
        if hasattr(context, 'variables') else {}

    for key in re.findall(r'\$+\w+', value):
        var_name = key[1:]
        value = value.replace(
            key,
            variables.get(
                var_name,
                os.environ.get(var_name, key)
            )
        )

    return value


def dereference_arguments(f):
    @wraps(f)
    def wrapper(context, *args, **kwargs):
        new_kwargs = {}
        new_args = []
        for key, value in kwargs.items():
            new_kwargs[key] = dereference_variables(context.text, value)
        for value in args:
            new_args.append(dereference_variables(context.text, value))
        context.processed_text = dereference_variables(context, context.text)\
            if context.text else ''
        return f(context, *new_args, **new_kwargs)
    return wrapper


def compare_lists(expected_list, actual_list, path=None):
    assert type(expected_list) is list,\
        "Expected {0} is not a list".format(repr(expected_list))
    assert type(actual_list) is list,\
        "Actual {0} is not a list".format(repr(actual_list))

    for i, item in enumerate(expected_list):
        path = '{0}.{1}'.format(path, i) if path else str(i)
        try:
            actual_value = actual_list[i]
        except ValueError:
            actual_value = None
        compare_values(item, actual_value, path=path)


def compare_dicts(expected_dict, actual_dict, path=None):
    assert type(expected_dict) is dict,\
        "Expected {0} is not a dict".format(repr(expected_dict))
    assert type(actual_dict) is dict,\
        "Actual {0} is not a dict".format(repr(actual_dict))

    for key in expected_dict:
        expected_value = expected_dict[key]
        actual_value = actual_dict.get(key, None)
        path = '{0}.{1}'.format(path, key) if path else key

        compare_values(expected_value, actual_value, path=path)


def validate_value(validator, value):
    if validator == 'int':
        return type(value) == int
    if validator == 'float':
        return type(value) == float
    if validator == 'number':
        return type(value) == int or type(value) == float
    raise Exception('Unknown validator: {}'.format(validator))


def compare_values(expected_value, actual_value, path=None):
    validator_pattern = r'^<is_(.+)>$'
    regex_pattern = r'^%(.+)%$'

    if type(expected_value) is dict:
        compare_dicts(expected_value, actual_value, path=path)
    elif type(expected_value) is list:
        compare_lists(expected_value, actual_value, path=path)
    elif isinstance(expected_value, string_type) and re.match(regex_pattern, expected_value):
        custom_regex = re.match(regex_pattern, expected_value).groups()[0]
        if not re.match(custom_regex, actual_value or ''):
            message = 'Expected {0} to match regex {1}'
            params = [repr(actual_value), repr(expected_value)]
            if path:
                message = message + ' at path {2}'
                params.append(path)
            raise AssertionError(message.format(*params))
    elif isinstance(expected_value, string_type) and re.match(validator_pattern, expected_value):
        validator_name = re.match(validator_pattern, expected_value).groups()[0]
        is_valid = validate_value(validator_name, actual_value)
        if not is_valid:
            message = 'Expected {0} to match validator {1}'
            params = [repr(actual_value), validator_name]
            if path:
                message = message + ' at path {2}'
                params.append(path)
            raise AssertionError(message.format(*params))
    else:
        try:
            assert expected_value == actual_value
        except AssertionError:
            message = 'Expected {0} to equal {1}'
            params = [repr(actual_value), repr(expected_value)]

            if path:
                message = message + ' at path {2}'
                params.append(path)

            raise AssertionError(message.format(*params))


def compare_contents(expected_value, actual_value):
    if expected_value[0] == '%' and expected_value[-1] == '%':
        assert re.search(expected_value.strip('%'), actual_value or ''),\
            'Expected response to contain regex \'{0}\''.format(expected_value)
    else:
        assert expected_value in actual_value,\
            'Expected response to contain text \'{0}\''.format(expected_value)


def do_request(context, method, endingpoint, body=None):
    fn = getattr(requests, method.lower())
    kwargs = {}

    if hasattr(context, 'request_headers'):
        kwargs['headers'] = context.request_headers

    if body:
        kwargs['data'] = body

    if hasattr(context, 'request_files'):
        kwargs['files'] = context.request_files

    context.response = fn(make_url(context, endingpoint), **kwargs)
