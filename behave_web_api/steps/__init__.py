import os
import json
import mimetypes
from behave import *
import difflib
from collections import OrderedDict

from behave_web_api.utils import (
    dereference_arguments,
    do_request,
    compare_values,
    compare_contents,
    get_nested_value,
    object_matches,
)


@given(u'I set header "{}" with value "{}"')
@dereference_arguments
def i_set_header_with_value(context, key, value):
    if not hasattr(context, 'request_headers'):
        context.request_headers = {}
    context.request_headers[key] = value


@given(u'I set variable "{}" with value "{}"')
@dereference_arguments
def i_set_variable_with_value(context, key, value):
    if not hasattr(context, 'variables'):
        context.variables = {}
    context.variables[key] = value


@given(u'I attach the file "{}" as "{}"')
@dereference_arguments
def i_attach_the_file_as(context, path, key):
    if not hasattr(context, 'request_files'):
        context.request_files = []
    name = os.path.basename(path)
    mimetype = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    context.request_files.append(
        (key, (name, open(path, 'rb'), mimetype))
    )


@when(u'I send a {} request to "{}" with body')
@dereference_arguments
def i_send_a_request_with_body(context, method, endingpoint):
    do_request(context, method, endingpoint, context.processed_text)


@when(u'I send a {} request to "{}" with body from file "{}"')
@dereference_arguments
def i_send_a_request_with_body_from_file(context, method, endingpoint, filename):
    with open(filename, 'r') as file:
        body = file.read().strip()
    do_request(context, method, endingpoint, body)


@when(u'I send a {} request to "{}" with values')
@dereference_arguments
def i_send_a_request_with_values(context, method, endingpoint):
    values = OrderedDict()

    for line in context.processed_text.split(u'\n'):
        pieces = line.split(u'=')
        values[pieces[0]] = ''.join(pieces[1:]) if len(pieces) > 1 else ''

    do_request(context, method, endingpoint, values)


@when(u'I send a {} request to "{}"')
@dereference_arguments
def i_send_a_request(context, method, endingpoint):
    do_request(context, method, endingpoint)


@then(u'the response code should be {}')
@dereference_arguments
def the_response_should_be(context, status_code):
    compare_values(int(status_code), context.response.status_code)


@then(u'the response should contain json')
@dereference_arguments
def the_response_should_contain_json(context):
    expected_data = json.loads(context.processed_text)
    actual_data = json.loads(context.response.text)
    compare_values(expected_data, actual_data)


@then(u'the response should contain text')
@dereference_arguments
def the_response_should_contain_text(context):
    compare_contents(context.processed_text, context.response.text)


@then(u'the response should have the exact same text')
@dereference_arguments
def the_response_should_contain_exact_text(context):
    a = context.processed_text
    b = context.response.text

    diff = list(difflib.ndiff(a.splitlines(), b.splitlines()))
    diff_string = "\n".join(diff)

    assert len(diff) == len(list(a.splitlines())), 'Texts are not the same:\n{}'.format(diff_string)


@then(u'print response')
def print_response(context):
    print(context.response.text)


@then(u'the response JSON at path "{json_path}" should contain an object with')
@dereference_arguments
def response_json_path_contains_object(context, json_path):
    """
    Search for an object with specified fields anywhere in an array at the given JSON path.
    The expected object is provided as a JSON doc string and performs partial matching.

    This step navigates to a JSON path and verifies that the array at that location
    contains at least one object matching the expected fields. The match is partial,
    meaning the actual objects can have additional fields not specified in the expected object.

    Args:
        context: Behave context containing the response and text
        json_path: Dot-separated path to the array (e.g., "data.users" or "items.0.tags")

    Example:
        Then the response JSON at path "data.users" should contain an object with
        '''
        {
            "name": "Alice",
            "address": {
                "country": "USA"
            }
        }
        '''
    """
    response_json = context.response.json()
    target_array = get_nested_value(response_json, json_path)
    expected_obj = json.loads(context.processed_text)

    assert target_array is not None, \
        f'Path "{json_path}" does not exist in response'

    assert isinstance(target_array, list), \
        f'Expected array at path "{json_path}" but got {type(target_array).__name__}'

    # Search for matching object in the array
    for item in target_array:
        if object_matches(item, expected_obj):
            return  # Found matching object

    # No matching object found - provide detailed error message consistent with compare_values
    actual_json = json.dumps(target_array, indent=2)
    expected_json = json.dumps(expected_obj, indent=2)
    assert False, \
        f'No object matching the expected value found at path "{json_path}"\n' \
        f'Expected to find object:\n{expected_json}\n' \
        f'Actual array at path "{json_path}":\n{actual_json}'
