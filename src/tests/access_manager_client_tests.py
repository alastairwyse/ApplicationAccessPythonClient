import unittest

from exceptions.element_not_found_error import ElementNotFoundError
from string_unique_stringifier import StringUniqueStringifier
from access_manager_client import AccessManagerClient

class AccessManagerClientUnitTests(unittest.TestCase):
    """Unit tests for the AccessManagerClient class."""

    def setUp(self):
        self._test_access_manager_client = AccessManagerClient[str, str, str, str](
            "http://127.0.0.1:5170/", 
            StringUniqueStringifier(), 
            StringUniqueStringifier(), 
            StringUniqueStringifier(), 
            StringUniqueStringifier()
        )


    def test_send_get_request_value_error(self):
        base_url: str = self._test_access_manager_client._base_url
        request_url: str = base_url + "userToGroupMappings/user/user1?includeIndirectMappings="

        with self.assertRaises(ValueError) as result:
            self._test_access_manager_client._send_get_request(request_url)

        self.assertEqual("One or more validation errors occurred.", str(result.exception))



    def test_send_get_request_element_not_found_error(self):
        base_url: str = self._test_access_manager_client._base_url
        request_url: str = base_url + "userToGroupMappings/user/invalid?includeIndirectMappings=false"

        with self.assertRaises(ElementNotFoundError) as result:
            self._test_access_manager_client._send_get_request(request_url)

        self.assertEqual("User 'invalid' does not exist. (Parameter 'user')", str(result.exception))



if __name__ == "__main__":
    unittest.main()
