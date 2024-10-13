from typing import List, Tuple

import unittest

from src.access_manager_string_element_client import AccessManagerStringElementClient

@unittest.skip("Integration tests not run by default")
class AccessManagerStringElementClientIntegrationTests(unittest.TestCase):
    """Integration tests for the AccessManagerStringElementClient class."""

    def setUp(self):
        self._test_access_manager_client = AccessManagerStringElementClient(
            "http://127.0.0.1:5170/"
        )

    def test_add_query_remove_elements_and_mappings(self):

        self._test_access_manager_client.add_user("user1")
        self._test_access_manager_client.add_group("group1")
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user1", "order", "view")

        all_users: List[str] = list(self._test_access_manager_client.users)
        self.assertEqual(1, len(all_users))
        self.assertTrue("user1" in all_users)

        all_groups: List[str] = list(self._test_access_manager_client.groups)
        self.assertEqual(1, len(all_groups))
        self.assertTrue("group1" in all_groups)

        user_component_mappings: List[Tuple[str, str]] = list(self._test_access_manager_client.get_user_to_application_component_and_access_level_mappings("user1"))
        self.assertEqual(1, len(user_component_mappings))
        self.assertTrue(("order", "view") in user_component_mappings)

        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user1", "order", "view")
        self._test_access_manager_client.remove_group("group1")
        self._test_access_manager_client.remove_user("user1")


if __name__ == "__main__":
    unittest.main()
