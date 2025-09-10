Behave Web Api
==============

|Build Status| |Version|

Provides testing for JSON APIs with Behave [1]_

Requires Python 3.11 or newer.

Installation
------------

::

    uv pip install behave-web-api

Import steps in your features/steps/__init__.py

.. code:: python

    from behave_web_api.steps import *

So you can use the steps in your feature files

.. code:: gherkin

    Feature: Doing http requests

      Scenario: Send text body and headers
        Given I set header "X-My-Header" with value "Something"
        And I set header "Content-Type" with value "application/json"
        When I send a POST request to "/requests/echo" with body:
        """
        {
            "a": 1,
            "b": "",
            "c": "0101",
            "d": "[01]+"
        }
        """
        Then the response code should be 200
        And the response should contain json:
        """
            {
                "headers": {
                    "X-My-Header": "Something"
                },
                "body": {
                    "a": "<is_number>",
                    "b": "%.*%",
                    "c": "%[01]+%",
                    "d": "[01]+"
                }
            }
        """

      Scenario: Send file using variables and environment variables
        Given I set the variable "DATA_DIR" with value "$PWD/features/data" 
        And I attach the file "$DATA_DIR/favicon.ico" as "upload"
        When I send a POST request to "/requests/echo"
        Then the response code should be 200
        And print response


And run using BASE_URL environment variable:

::

    BASE_URL=localhost:5000 behave features/requests.feature


Available Steps
---------------

-  Given I set variable "{}" with value "{}"
-  Given I set header "{}" with value "{}"
-  Given I attach the file "{}" as "{}"
-  When I send a {} request to "{}" with body:
-  When I send a {} request to "{}" with values:
-  When I send a {} request to "{}"
-  Then the response code should be {}
-  Then the response should contain json:
-  Then the response should contain text:
-  Then print response


Acknowledgments
---------------

The REST steps are based on Behat WebApiExtension [2]_

.. [1] http://pythonhosted.org/behave/

.. [2] https://github.com/Behat/WebApiExtension

.. |Build Status| image:: https://travis-ci.org/jefersondaniel/behave-web-api.svg
   :target: https://travis-ci.org/jefersondaniel/behave-web-api

.. |Version| image:: https://badge.fury.io/py/behave-web-api.svg
   :target: https://pypi.python.org/pypi/behave-web-api
