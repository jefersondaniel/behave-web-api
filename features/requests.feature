Feature: Doing http requests

  Scenario: Send text body and headers
    Given I set header "X-My-Header" with value "Something"
    When I send a POST request to "/requests/echo" with body:
    """
    Something
    """
    Then the response code should be 200
    And the response should contain json:
    """
        {
            "method": "POST",
            "headers": {
                "X-My-Header": "Something"
            },
            "body": "Something"
        }
    """

  Scenario: Send form data
    Given I set header "X-My-Header" with value "Something"
    When I send a POST request to "/requests/echo" with values:
    """
    name=Wilson
    age=42
    """
    Then the response should contain json:
    """
        {
            "method": "POST",
            "body": "name=Wilson&age=42"
        }
    """

  Scenario: Send file
    Given I set header "X-My-Header" with value "Something"
    And I attach the file "$PWD/features/data/favicon.ico" as "upload"
    When I send a POST request to "/requests/echo"
    Then the response should contain json:
    """
        {
            "method": "POST",
            "files": [
                {
                    "key": "upload",
                    "name": "favicon.ico"
                }
            ]
        }
    """

  Scenario: Set variable
    Given I set variable "username" with value "Bob"
    When I send a POST request to "/requests/echo" with body:
    """
    Hello $username
    """
    Then the response should contain json:
    """
        {
            "body": "Hello Bob"
        }
    """

  Scenario: Set variable from file
    When I send a POST request to "/requests/echo" with body from file "$PWD/features/data/body.txt"
    Then the response should contain json:
    """
        {
            "body": "Hello World"
        }
    """
    Then print response

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
            "method": "POST",
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

  Scenario: Verify JSON path contains object with partial match
    Given I set header "Content-Type" with value "application/json"
    When I send a POST request to "/requests/echo" with body:
    """
    {
        "data": {
            "users": [
                {
                    "id": 1,
                    "name": "Alice",
                    "email": "alice@example.com",
                    "address": {
                        "city": "New York",
                        "country": "USA"
                    }
                },
                {
                    "id": 2,
                    "name": "Bob",
                    "email": "bob@example.com",
                    "address": {
                        "city": "London",
                        "country": "UK"
                    }
                },
                {
                    "id": 3,
                    "name": "Charlie",
                    "email": "charlie@example.com",
                    "address": {
                        "city": "Toronto",
                        "country": "Canada"
                    }
                }
            ]
        }
    }
    """
    Then the response code should be 200
    And the response JSON at path "body.data.users" should contain an object with:
    """
    {
        "name": "Bob",
        "address": {
            "country": "UK"
        }
    }
    """
    And the response JSON at path "body.data.users" should contain an object with:
    """
    {
        "id": 1,
        "name": "Alice"
    }
    """
    And the response JSON at path "body.data.users" should contain an object with:
    """
    {
        "address": {
            "city": "Toronto"
        }
    }
    """
