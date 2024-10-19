#
# Copyright 2024 Alastair Wyse (https://github.com/alastairwyse/ApplicationAccessPythonClient/)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

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
