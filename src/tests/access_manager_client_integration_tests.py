from typing import List, Tuple, Set
import unittest

from application_screen import ApplicationScreen
from access_level import AccessLevel
from exceptions.element_not_found_error import ElementNotFoundError
from unique_stringifier_base import UniqueStringifierBase
from string_unique_stringifier import StringUniqueStringifier
from access_manager_client import AccessManagerClient

#@unittest.skip("Need to be run manually in a specific order")
class AccessManagerClientIntegrationTests(unittest.TestCase):
    """Integration tests for the AccessManagerClient class."""

    _URL_RESERVED_CHARACTERS: str = "! * ' ( ) ; : @ & = + $ , / ? % # [ ]"

    # Entity string constants
    _CLIENT_ACCOUNTS: str = "ClientAccount"
    _COMPANY_1: str = "Company1"
    _COMPANY_2: str = "Company2"
    _COMPANY_3: str = "Company3"
    _COMPANY_4: str = "Company4"
    _COMPANY_5: str = "Company5"
    _COMPANY_6: str = "Company6"
    _COMPANY_7: str = "Company7"
    _COMPANY_8: str = "Company8"
    _COMPANY_9: str = "Company9"
    _COMPANY_10: str = "Company10"
    _PRODUCT_LINES: str = "ProductLines"
    _LINE_1: str = "Line1"
    _LINE_2: str = "Line2"
    _LINE_3: str = "Line3"
    _LINE_4: str = "Line4"
    _LINE_5: str = "Line5"
    _LINE_6: str = "Line6"
    _LINE_7: str = "Line7"
    _LINE_8: str = "Line8"
    _LINE_9: str = "Line9"
    _LINE_10: str = "Line10"
    _UNMAPPED: str = "Unmapped"


    def setUp(self):
        self._test_access_manager_client = AccessManagerClient[str, str, ApplicationScreen, AccessLevel](
            "http://127.0.0.1:5170/", 
            StringUniqueStringifier(), 
            StringUniqueStringifier(), 
            self._ApplicationScreenUniqueStringifier(), 
            self._AccessLevelUniqueStringifier()
        )

    
    def test_connection_exceptions(self):

        self._test_access_manager_client = AccessManagerClient[str, str, ApplicationScreen, AccessLevel](
            "http://127.0.0.1:100/", 
            StringUniqueStringifier(), 
            StringUniqueStringifier(), 
            self._ApplicationScreenUniqueStringifier(), 
            self._AccessLevelUniqueStringifier()
        )

        with self.assertRaises(Exception) as result:
            self._test_access_manager_client.users

        self.assertEqual("Failed to call URL 'http://127.0.0.1:100/api/v1/users' with 'GET' method.", str(result.exception))

        with self.assertRaises(Exception) as result:
            self._test_access_manager_client.contains_user("user1")

        self.assertEqual("Failed to call URL 'http://127.0.0.1:100/api/v1/users/user1' with 'GET' method.", str(result.exception))

        with self.assertRaises(Exception) as result:
            self._test_access_manager_client.add_user("user1")

        self.assertEqual("Failed to call URL 'http://127.0.0.1:100/api/v1/users/user1' with 'POST' method.", str(result.exception))

        with self.assertRaises(Exception) as result:
            self._test_access_manager_client.remove_user("user1")

        self.assertEqual("Failed to call URL 'http://127.0.0.1:100/api/v1/users/user1' with 'DELETE' method.", str(result.exception))


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


    def tests_url_reserved_characters(self):

        self._test_access_manager_client.add_user(self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.add_group(self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.add_group("group1")
        self._test_access_manager_client.add_group("group2")
        self._test_access_manager_client.add_user_to_group_mapping(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.add_group_to_group_mapping(self._URL_RESERVED_CHARACTERS, "group1")
        self._test_access_manager_client.add_group_to_group_mapping("group2",  self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping(self._URL_RESERVED_CHARACTERS, ApplicationScreen.reserved_characters, AccessLevel.reserved_characters)
        self._test_access_manager_client.add_group_to_application_component_and_access_level_mapping(self._URL_RESERVED_CHARACTERS, ApplicationScreen.reserved_characters, AccessLevel.reserved_characters)
        self._test_access_manager_client.add_entity_type(self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.add_entity(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.add_user_to_entity_mapping(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.add_group_to_entity_mapping(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)

        contains_result: bool = self._test_access_manager_client.contains_user(self._URL_RESERVED_CHARACTERS)
        self.assertTrue(contains_result)
        containsResult = self._test_access_manager_client.contains_group(self._URL_RESERVED_CHARACTERS)
        self.assertTrue(containsResult)
        user_to_group_gappings: List[str] = list(self._test_access_manager_client.get_user_to_group_mappings(self._URL_RESERVED_CHARACTERS, False))
        self.assertEqual(1, len(user_to_group_gappings))
        group_to_user_mappings: List[str] = list(self._test_access_manager_client.get_group_to_user_mappings(self._URL_RESERVED_CHARACTERS, False))
        self.assertEqual(1, len(group_to_user_mappings))
        group_to_group_mappings: List[str] = list(self._test_access_manager_client.get_group_to_group_mappings(self._URL_RESERVED_CHARACTERS, False))
        self.assertEqual(1, len(group_to_group_mappings))
        group_to_group_reverse_mappings: List[str] = list(self._test_access_manager_client.get_group_to_group_reverse_mappings(self._URL_RESERVED_CHARACTERS, False))
        self.assertEqual(1, len(group_to_group_reverse_mappings))
        user_component_mappings: List[Tuple[ApplicationScreen, AccessLevel]] = list(self._test_access_manager_client.get_user_to_application_component_and_access_level_mappings(self._URL_RESERVED_CHARACTERS))
        self.assertEqual(1, len(user_component_mappings))
        users: List[str] = list(self._test_access_manager_client.get_application_component_and_access_level_to_user_mappings(ApplicationScreen.reserved_characters, AccessLevel.reserved_characters, False))
        self.assertEqual(1, len(users))
        group_component_mappings: List[Tuple[ApplicationScreen, AccessLevel]] = list(self._test_access_manager_client.get_group_to_application_component_and_access_level_mappings(self._URL_RESERVED_CHARACTERS))
        self.assertEqual(1, len(group_component_mappings))
        groups: List[str] = list(self._test_access_manager_client.get_application_component_and_access_level_to_group_mappings(ApplicationScreen.reserved_characters, AccessLevel.reserved_characters, False))
        self.assertEqual(1, len(groups))
        contains_result = self._test_access_manager_client.contains_entity_type(self._URL_RESERVED_CHARACTERS)
        self.assertTrue(contains_result)
        entities: List[str] = list(self._test_access_manager_client.get_entities(self._URL_RESERVED_CHARACTERS))
        self.assertEqual(1, len(entities))
        contains_result = self._test_access_manager_client.contains_entity(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self.assertTrue(contains_result)
        user_entity_mappings: List[Tuple[str, str]] = list(self._test_access_manager_client.get_user_to_entity_mappings(self._URL_RESERVED_CHARACTERS))
        self.assertEqual(1, len(user_entity_mappings))
        entities: List[str] = list(self._test_access_manager_client.get_user_to_entity_mappings_for_type(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS))
        self.assertEqual(1, len(entities))
        users: List[str] = list(self._test_access_manager_client.get_entity_to_user_mappings(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS, False))
        self.assertEqual(1, len(users))
        group_entity_mappings: List[Tuple[str, str]] = list(self._test_access_manager_client.get_group_to_entity_mappings(self._URL_RESERVED_CHARACTERS))
        self.assertEqual(1, len(group_entity_mappings))
        entities = list(self._test_access_manager_client.get_group_to_entity_mappings_for_type(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS))
        self.assertEqual(1, len(entities))
        groups = list(self._test_access_manager_client.get_entity_to_group_mappings(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS, False))
        self.assertEqual(1, len(groups))
        has_access_result: bool = self._test_access_manager_client.has_access_to_application_component(self._URL_RESERVED_CHARACTERS, ApplicationScreen.reserved_characters, AccessLevel.reserved_characters)
        self.assertTrue(has_access_result)
        has_access_result = self._test_access_manager_client.has_access_to_entity(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self.assertTrue(has_access_result)
        user_component_mappings_set: Set[Tuple[ApplicationScreen, AccessLevel]] = self._test_access_manager_client.get_application_components_accesible_by_user(self._URL_RESERVED_CHARACTERS)
        self.assertEqual(1, len(user_component_mappings_set))
        group_component_mappings_set: Set[Tuple[ApplicationScreen, AccessLevel]] = self._test_access_manager_client.get_application_components_accesible_by_group(self._URL_RESERVED_CHARACTERS)
        self.assertEqual(1, len(group_component_mappings_set))
        user_entity_mappings_set = self._test_access_manager_client.get_entities_accessible_by_user(self._URL_RESERVED_CHARACTERS)
        self.assertEqual(1, len(user_entity_mappings_set))
        entities_set: Set[str] = self._test_access_manager_client.get_entities_of_type_accessible_by_user(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self.assertEqual(1, len(entities_set))
        group_entity_mappings_set: Set[Tuple[str, str]] = self._test_access_manager_client.get_entities_accessible_by_group(self._URL_RESERVED_CHARACTERS)
        self.assertEqual(1, len(group_entity_mappings_set))
        entities_set = self._test_access_manager_client.get_entities_of_type_accessible_by_group(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self.assertEqual(1, len(entities_set))

        self._test_access_manager_client.remove_group_to_entity_mapping(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.remove_user_to_entity_mapping(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.remove_entity(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.remove_entity_type(self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.remove_group_to_application_component_and_access_level_mapping(self._URL_RESERVED_CHARACTERS, ApplicationScreen.reserved_characters, AccessLevel.reserved_characters)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping(self._URL_RESERVED_CHARACTERS, ApplicationScreen.reserved_characters, AccessLevel.reserved_characters)
        self._test_access_manager_client.remove_group_to_group_mapping("group2",  self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.remove_group_to_group_mapping(self._URL_RESERVED_CHARACTERS, "group1")
        self._test_access_manager_client.remove_user_to_group_mapping(self._URL_RESERVED_CHARACTERS, self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.remove_group("group2")
        self._test_access_manager_client.remove_group("group1")
        self._test_access_manager_client.remove_group(self._URL_RESERVED_CHARACTERS)
        self._test_access_manager_client.remove_user(self._URL_RESERVED_CHARACTERS)
       

    def test_property_gets_on_empty_access_manager(self):

        result: List[str] = list(self._test_access_manager_client.users)
        self.assertEqual(0, len(result))

        result = list(self._test_access_manager_client.groups)
        self.assertEqual(0, len(result))

        result = list(self._test_access_manager_client.entity_types)
        self.assertEqual(0, len(result))


    def test_add_elements_and_mappings(self):

        self._test_access_manager_client.add_user("user1")
        self._test_access_manager_client.add_user("user2")
        self._test_access_manager_client.add_user("user3")
        self._test_access_manager_client.add_user("user4")
        self._test_access_manager_client.add_user("user5")
        self._test_access_manager_client.add_user("user6")
        self._test_access_manager_client.add_user("user7")
        self._test_access_manager_client.add_user("user8")
        self._test_access_manager_client.add_user("user9")
        self._test_access_manager_client.add_user("user10")
        self._test_access_manager_client.add_user("user11")
        self._test_access_manager_client.add_user("user12")
        self._test_access_manager_client.add_user("unmappedUser1")
        self._test_access_manager_client.add_user("orphanedUser")

        self._test_access_manager_client.add_group("group1")
        self._test_access_manager_client.add_group("group2")
        self._test_access_manager_client.add_group("group3")
        self._test_access_manager_client.add_group("group4")
        self._test_access_manager_client.add_group("group5")
        self._test_access_manager_client.add_group("group6")
        self._test_access_manager_client.add_group("unmappedGroup1")
        self._test_access_manager_client.add_group("unmappedGroup2")
        self._test_access_manager_client.add_group("orphanedGroup")

        self._test_access_manager_client.add_entity_type(self._CLIENT_ACCOUNTS)
        self._test_access_manager_client.add_entity_type(self._PRODUCT_LINES)
        self._test_access_manager_client.add_entity_type(self._UNMAPPED)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_1)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_2)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_3)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_4)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_5)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_6)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_7)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_8)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_9)
        self._test_access_manager_client.add_entity(self._CLIENT_ACCOUNTS, self._COMPANY_10)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_1)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_2)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_3)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_4)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_5)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_6)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_7)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_8)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_9)
        self._test_access_manager_client.add_entity(self._PRODUCT_LINES, self._LINE_10)

        self._test_access_manager_client.add_user_to_group_mapping("user1", "group1")
        self._test_access_manager_client.add_user_to_group_mapping("user2", "group1")
        self._test_access_manager_client.add_user_to_group_mapping("user3", "group2")
        self._test_access_manager_client.add_user_to_group_mapping("user4", "group2")
        self._test_access_manager_client.add_user_to_group_mapping("user5", "group3")
        self._test_access_manager_client.add_user_to_group_mapping("user6", "group3")
        self._test_access_manager_client.add_user_to_group_mapping("user7", "group4")
        self._test_access_manager_client.add_user_to_group_mapping("user8", "group4")
        self._test_access_manager_client.add_user_to_group_mapping("user9", "group5")
        self._test_access_manager_client.add_user_to_group_mapping("user10", "group5")
        self._test_access_manager_client.add_user_to_group_mapping("user11", "group6")
        self._test_access_manager_client.add_user_to_group_mapping("user12", "group6")
        self._test_access_manager_client.add_user_to_group_mapping("unmappedUser1", "unmappedGroup1")

        self._test_access_manager_client.add_group_to_group_mapping("group1", "group3")
        self._test_access_manager_client.add_group_to_group_mapping("group1", "group4")
        self._test_access_manager_client.add_group_to_group_mapping("group2", "group4")
        self._test_access_manager_client.add_group_to_group_mapping("group3", "group5")
        self._test_access_manager_client.add_group_to_group_mapping("group4", "group5")
        self._test_access_manager_client.add_group_to_group_mapping("group4", "group6")
        self._test_access_manager_client.add_group_to_group_mapping("unmappedGroup1", "unmappedGroup2")

        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user1", ApplicationScreen.order, AccessLevel.view)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user1", ApplicationScreen.order, AccessLevel.create)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user2", ApplicationScreen.order, AccessLevel.modify)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user3", ApplicationScreen.order, AccessLevel.delete)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user4", ApplicationScreen.summary, AccessLevel.view)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user5", ApplicationScreen.summary, AccessLevel.create)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user6", ApplicationScreen.summary, AccessLevel.modify)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user7", ApplicationScreen.summary, AccessLevel.delete)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user8", ApplicationScreen.manage_products, AccessLevel.view)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user9", ApplicationScreen.manage_products, AccessLevel.create)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user10", ApplicationScreen.manage_products, AccessLevel.modify)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user11", ApplicationScreen.manage_products, AccessLevel.delete)
        self._test_access_manager_client.add_user_to_application_component_and_access_level_mapping("user12", ApplicationScreen.settings, AccessLevel.view)

        self._test_access_manager_client.add_group_to_application_component_and_access_level_mapping("group1", ApplicationScreen.settings, AccessLevel.create)
        self._test_access_manager_client.add_group_to_application_component_and_access_level_mapping("group1", ApplicationScreen.settings, AccessLevel.modify)
        self._test_access_manager_client.add_group_to_application_component_and_access_level_mapping("group2", ApplicationScreen.settings, AccessLevel.delete)
        self._test_access_manager_client.add_group_to_application_component_and_access_level_mapping("group3", ApplicationScreen.delivery, AccessLevel.view)
        self._test_access_manager_client.add_group_to_application_component_and_access_level_mapping("group4", ApplicationScreen.delivery, AccessLevel.create)
        self._test_access_manager_client.add_group_to_application_component_and_access_level_mapping("group5", ApplicationScreen.delivery, AccessLevel.modify)
        self._test_access_manager_client.add_group_to_application_component_and_access_level_mapping("group6", ApplicationScreen.delivery, AccessLevel.delete)

        self._test_access_manager_client.add_user_to_entity_mapping("user1", self._CLIENT_ACCOUNTS, self._COMPANY_1)
        self._test_access_manager_client.add_user_to_entity_mapping("user1", self._CLIENT_ACCOUNTS, self._COMPANY_2)
        self._test_access_manager_client.add_user_to_entity_mapping("user2", self._CLIENT_ACCOUNTS, self._COMPANY_3)
        self._test_access_manager_client.add_user_to_entity_mapping("user3", self._CLIENT_ACCOUNTS, self._COMPANY_4)
        self._test_access_manager_client.add_user_to_entity_mapping("user4", self._CLIENT_ACCOUNTS, self._COMPANY_5)
        self._test_access_manager_client.add_user_to_entity_mapping("user5", self._CLIENT_ACCOUNTS, self._COMPANY_6)
        self._test_access_manager_client.add_user_to_entity_mapping("user6", self._CLIENT_ACCOUNTS, self._COMPANY_7)
        self._test_access_manager_client.add_user_to_entity_mapping("user7", self._CLIENT_ACCOUNTS, self._COMPANY_8)
        self._test_access_manager_client.add_user_to_entity_mapping("user8", self._CLIENT_ACCOUNTS, self._COMPANY_9)
        self._test_access_manager_client.add_user_to_entity_mapping("user9", self._CLIENT_ACCOUNTS, self._COMPANY_10)
        self._test_access_manager_client.add_user_to_entity_mapping("user10", self._PRODUCT_LINES, self._LINE_1)
        self._test_access_manager_client.add_user_to_entity_mapping("user11", self._PRODUCT_LINES, self._LINE_2)
        self._test_access_manager_client.add_user_to_entity_mapping("user12", self._PRODUCT_LINES, self._LINE_3)

        self._test_access_manager_client.add_group_to_entity_mapping("group1", self._PRODUCT_LINES, self._LINE_4)
        self._test_access_manager_client.add_group_to_entity_mapping("group1", self._PRODUCT_LINES, self._LINE_5)
        self._test_access_manager_client.add_group_to_entity_mapping("group2", self._PRODUCT_LINES, self._LINE_6)
        self._test_access_manager_client.add_group_to_entity_mapping("group3", self._PRODUCT_LINES, self._LINE_7)
        self._test_access_manager_client.add_group_to_entity_mapping("group4", self._PRODUCT_LINES, self._LINE_8)
        self._test_access_manager_client.add_group_to_entity_mapping("group5", self._PRODUCT_LINES, self._LINE_9)
        self._test_access_manager_client.add_group_to_entity_mapping("group6", self._PRODUCT_LINES, self._LINE_10)
        self._test_access_manager_client.add_group_to_entity_mapping("group6", self._CLIENT_ACCOUNTS, self._COMPANY_1)


    def test_queries(self):

        all_users: List[str] = list(self._test_access_manager_client.users)
        self.assertEqual(14, len(all_users))
        self.assertTrue("user1" in all_users)
        self.assertTrue("user2" in all_users)
        self.assertTrue("user3" in all_users)
        self.assertTrue("user4" in all_users)
        self.assertTrue("user5" in all_users)
        self.assertTrue("user6" in all_users)
        self.assertTrue("user7" in all_users)
        self.assertTrue("user8" in all_users)
        self.assertTrue("user9" in all_users)
        self.assertTrue("user10" in all_users)
        self.assertTrue("user11" in all_users)
        self.assertTrue("user12" in all_users)
        self.assertTrue("unmappedUser1" in all_users)
        self.assertTrue("orphanedUser" in all_users)
        
        all_groups: List[str] = list(self._test_access_manager_client.groups)
        self.assertTrue("group1" in all_groups)
        self.assertTrue("group2" in all_groups)
        self.assertTrue("group3" in all_groups)
        self.assertTrue("group4" in all_groups)
        self.assertTrue("group5" in all_groups)
        self.assertTrue("group6" in all_groups)
        self.assertTrue("unmappedGroup1" in all_groups)
        self.assertTrue("unmappedGroup2" in all_groups)
        self.assertTrue("orphanedGroup" in all_groups)
        
        all_entity_types: List[str] = list(self._test_access_manager_client.entity_types)
        self.assertEqual(3, len(all_entity_types))
        self.assertTrue(self._CLIENT_ACCOUNTS in all_entity_types)
        self.assertTrue(self._PRODUCT_LINES in all_entity_types)
        self.assertTrue(self._UNMAPPED in all_entity_types)

        contains_result: bool = self._test_access_manager_client.contains_user("user1")
        self.assertTrue(contains_result)
        containsResult = self._test_access_manager_client.contains_user("user99")
        self.assertFalse(containsResult)

        containsResult = self._test_access_manager_client.contains_group("group1")
        self.assertTrue(containsResult)
        containsResult = self._test_access_manager_client.contains_group("group99")
        self.assertFalse(containsResult)

        user_to_group_gappings: List[str] = list(self._test_access_manager_client.get_user_to_group_mappings("user5", False))
        self.assertEqual(1, len(user_to_group_gappings))
        self.assertTrue("group3" in user_to_group_gappings)
        user_to_group_gappings = list(self._test_access_manager_client.get_user_to_group_mappings("user5", True))
        self.assertEqual(2, len(user_to_group_gappings))
        self.assertTrue("group3" in user_to_group_gappings)
        self.assertTrue("group5" in user_to_group_gappings)
        user_to_group_gappings = list(self._test_access_manager_client.get_user_to_group_mappings("orphanedUser", False))
        self.assertEqual(0, len(user_to_group_gappings))

        group_to_user_mappings: List[str] = list(self._test_access_manager_client.get_group_to_user_mappings("group3", False))
        self.assertEqual(2, len(group_to_user_mappings))
        self.assertTrue("user5" in group_to_user_mappings)
        self.assertTrue("user6" in group_to_user_mappings)
        group_to_user_mappings = list(self._test_access_manager_client.get_group_to_user_mappings("group3", True))
        self.assertEqual(4, len(group_to_user_mappings))
        self.assertTrue("user1" in group_to_user_mappings)
        self.assertTrue("user2" in group_to_user_mappings)
        self.assertTrue("user5" in group_to_user_mappings)
        self.assertTrue("user6" in group_to_user_mappings)
        group_to_user_mappings = list(self._test_access_manager_client.get_group_to_user_mappings("orphanedGroup", False))
        self.assertEqual(0, len(group_to_user_mappings))

        group_to_group_mappings: List[str] = list(self._test_access_manager_client.get_group_to_group_mappings("group2", False))
        self.assertEqual(1, len(group_to_group_mappings))
        self.assertTrue("group4" in group_to_group_mappings)
        group_to_group_mappings = list(self._test_access_manager_client.get_group_to_group_mappings("group2", True))
        self.assertEqual(3, len(group_to_group_mappings))
        self.assertTrue("group4" in group_to_group_mappings)
        self.assertTrue("group5" in group_to_group_mappings)
        self.assertTrue("group6" in group_to_group_mappings)
        group_to_group_mappings = list(self._test_access_manager_client.get_group_to_group_mappings("orphanedGroup", False))
        self.assertEqual(0, len(group_to_group_mappings))

        group_to_group_reverse_mappings: List[str] = list(self._test_access_manager_client.get_group_to_group_reverse_mappings("group6", False))
        self.assertEqual(1, len(group_to_group_reverse_mappings))
        self.assertTrue("group4" in group_to_group_reverse_mappings)
        group_to_group_reverse_mappings = list(self._test_access_manager_client.get_group_to_group_reverse_mappings("group6", True))
        self.assertEqual(3, len(group_to_group_reverse_mappings))
        self.assertTrue("group1" in group_to_group_reverse_mappings)
        self.assertTrue("group2" in group_to_group_reverse_mappings)
        self.assertTrue("group4" in group_to_group_reverse_mappings)
        group_to_group_reverse_mappings = list(self._test_access_manager_client.get_group_to_group_reverse_mappings("orphanedGroup", False))
        self.assertEqual(0, len(group_to_group_reverse_mappings))

        user_component_mappings: List[Tuple[ApplicationScreen, AccessLevel]] = list(self._test_access_manager_client.get_user_to_application_component_and_access_level_mappings("user5"))
        self.assertEqual(1, len(user_component_mappings))
        self.assertTrue((ApplicationScreen.summary, AccessLevel.create) in user_component_mappings)
        user_component_mappings = list(self._test_access_manager_client.get_user_to_application_component_and_access_level_mappings("orphanedUser"))
        self.assertEqual(0, len(user_component_mappings))

        users: List[str] = list(self._test_access_manager_client.get_application_component_and_access_level_to_user_mappings(ApplicationScreen.settings, AccessLevel.view, False))
        self.assertEqual(1, len(users))
        self.assertTrue("user12" in users)
        users = list(self._test_access_manager_client.get_application_component_and_access_level_to_user_mappings(ApplicationScreen.delivery, AccessLevel.view, True))
        self.assertEqual(4, len(users))
        self.assertTrue("user1" in users)
        self.assertTrue("user2" in users)
        self.assertTrue("user5" in users)
        self.assertTrue("user6" in users)
        users = list(self._test_access_manager_client.get_application_component_and_access_level_to_user_mappings(ApplicationScreen.delivery, AccessLevel.view, False))
        self.assertEqual(0, len(users))

        group_component_mappings: List[Tuple[ApplicationScreen, AccessLevel]] = list(self._test_access_manager_client.get_group_to_application_component_and_access_level_mappings("group4"))
        self.assertEqual(1, len(group_component_mappings))
        self.assertTrue((ApplicationScreen.delivery, AccessLevel.create) in group_component_mappings)
        group_component_mappings = list(self._test_access_manager_client.get_group_to_application_component_and_access_level_mappings("orphanedGroup"))
        self.assertEqual(0, len(group_component_mappings))

        groups: List[str] = list(self._test_access_manager_client.get_application_component_and_access_level_to_group_mappings(ApplicationScreen.delivery, AccessLevel.view, False))
        self.assertEqual(1, len(groups))
        self.assertTrue("group3" in groups)
        groups = list(self._test_access_manager_client.get_application_component_and_access_level_to_group_mappings(ApplicationScreen.delivery, AccessLevel.view, True))
        self.assertEqual(2, len(groups))
        self.assertTrue("group1" in groups)
        self.assertTrue("group3" in groups)
        groups = list(self._test_access_manager_client.get_application_component_and_access_level_to_group_mappings(ApplicationScreen.summary, AccessLevel.view, False))
        self.assertEqual(0, len(groups))

        contains_result = self._test_access_manager_client.contains_entity_type(self._PRODUCT_LINES)
        self.assertTrue(contains_result)
        contains_result = self._test_access_manager_client.contains_entity_type("Invalid")
        self.assertFalse(contains_result)

        entities: List[str] = list(self._test_access_manager_client.get_entities(self._PRODUCT_LINES))
        self.assertEqual(10, len(entities))
        self.assertTrue(self._LINE_1 in entities)
        self.assertTrue(self._LINE_2 in entities)
        self.assertTrue(self._LINE_3 in entities)
        self.assertTrue(self._LINE_4 in entities)
        self.assertTrue(self._LINE_5 in entities)
        self.assertTrue(self._LINE_6 in entities)
        self.assertTrue(self._LINE_7 in entities)
        self.assertTrue(self._LINE_8 in entities)
        self.assertTrue(self._LINE_9 in entities)
        self.assertTrue(self._LINE_10 in entities)
        entities = list(self._test_access_manager_client.get_entities(self._UNMAPPED))
        self.assertEqual(0, len(entities))

        contains_result = self._test_access_manager_client.contains_entity(self._PRODUCT_LINES, self._LINE_1)
        self.assertTrue(contains_result)
        contains_result = self._test_access_manager_client.contains_entity(self._PRODUCT_LINES, "Invalid")
        self.assertFalse(contains_result)

        user_entity_mappings: List[Tuple[str, str]] = list(self._test_access_manager_client.get_user_to_entity_mappings("user6"))
        self.assertEqual(1, len(user_entity_mappings))
        self.assertTrue((self._CLIENT_ACCOUNTS, self._COMPANY_7) in user_entity_mappings)
        user_entity_mappings = list(self._test_access_manager_client.get_user_to_entity_mappings("orphanedUser"))
        self.assertEqual(0, len(user_entity_mappings))

        entities: List[str] = list(self._test_access_manager_client.get_user_to_entity_mappings_for_type("user3", self._CLIENT_ACCOUNTS))
        self.assertEqual(1, len(entities))
        self.assertTrue("Company4" in entities)
        entities = list(self._test_access_manager_client.get_user_to_entity_mappings_for_type("orphanedUser", self._CLIENT_ACCOUNTS))
        self.assertEqual(0, len(entities))

        users: List[str] = list(self._test_access_manager_client.get_entity_to_user_mappings(self._CLIENT_ACCOUNTS, self._COMPANY_1, False))
        self.assertEqual(1, len(users))
        self.assertTrue("user1" in users)
        users = list(self._test_access_manager_client.get_entity_to_user_mappings(self._CLIENT_ACCOUNTS, self._COMPANY_1, True))
        self.assertEqual(8, len(users))
        self.assertTrue("user1" in users)
        self.assertTrue("user2" in users)
        self.assertTrue("user3" in users)
        self.assertTrue("user4" in users)
        self.assertTrue("user7" in users)
        self.assertTrue("user8" in users)
        self.assertTrue("user11" in users)
        self.assertTrue("user12" in users)
        users = list(self._test_access_manager_client.get_entity_to_user_mappings(self._PRODUCT_LINES, self._LINE_10, False))
        self.assertEqual(0, len(users))

        group_entity_mappings: List[Tuple[str, str]] = list(self._test_access_manager_client.get_group_to_entity_mappings("group4"))
        self.assertEqual(1, len(group_entity_mappings))
        self.assertTrue((self._PRODUCT_LINES, self._LINE_8) in group_entity_mappings)
        group_entity_mappings = list(self._test_access_manager_client.get_group_to_entity_mappings("orphanedGroup"))
        self.assertEqual(0, len(group_entity_mappings))

        entities = list(self._test_access_manager_client.get_group_to_entity_mappings_for_type("group2", self._PRODUCT_LINES))
        self.assertEqual(1, len(entities))
        self.assertTrue(self._LINE_6 in entities)
        entities = list(self._test_access_manager_client.get_group_to_entity_mappings_for_type("orphanedGroup", self._PRODUCT_LINES))
        self.assertEqual(0, len(entities))
        
        groups = list(self._test_access_manager_client.get_entity_to_group_mappings(self._CLIENT_ACCOUNTS, self._COMPANY_1, False))
        self.assertEqual(1, len(groups))
        self.assertTrue("group6" in groups)
        groups = list(self._test_access_manager_client.get_entity_to_group_mappings(self._CLIENT_ACCOUNTS, self._COMPANY_1, True))
        self.assertEqual(4, len(groups))
        self.assertTrue("group1" in groups)
        self.assertTrue("group2" in groups)
        self.assertTrue("group4" in groups)
        self.assertTrue("group6" in groups)
        groups = list(self._test_access_manager_client.get_entity_to_group_mappings(self._CLIENT_ACCOUNTS, self._COMPANY_2, False))
        self.assertEqual(0, len(groups))

        has_access_result: bool = self._test_access_manager_client.has_access_to_application_component("user1", ApplicationScreen.order, AccessLevel.view)
        self.assertTrue(has_access_result)
        has_access_result = self._test_access_manager_client.has_access_to_application_component("user12", ApplicationScreen.order, AccessLevel.view)
        self.assertFalse(has_access_result)

        has_access_result = self._test_access_manager_client.has_access_to_entity("user1", self._CLIENT_ACCOUNTS, self._COMPANY_1)
        self.assertTrue(has_access_result)
        has_access_result = self._test_access_manager_client.has_access_to_entity("user12", self._CLIENT_ACCOUNTS, self._COMPANY_2)
        self.assertFalse(has_access_result)

        user_component_mappings_set: Set[Tuple[ApplicationScreen, AccessLevel]] = self._test_access_manager_client.get_application_components_accesible_by_user("user8")
        self.assertEqual(4, len(user_component_mappings_set))
        self.assertTrue((ApplicationScreen.manage_products, AccessLevel.view) in user_component_mappings_set)
        self.assertTrue((ApplicationScreen.delivery, AccessLevel.create) in user_component_mappings_set)
        self.assertTrue((ApplicationScreen.delivery, AccessLevel.delete) in user_component_mappings_set)
        self.assertTrue((ApplicationScreen.delivery, AccessLevel.modify) in user_component_mappings_set)
        user_component_mappings_set = self._test_access_manager_client.get_application_components_accesible_by_user("orphanedUser")
        self.assertEqual(0, len(user_component_mappings_set))

        group_component_mappings_set: Set[Tuple[ApplicationScreen, AccessLevel]] = self._test_access_manager_client.get_application_components_accesible_by_group("group4")
        self.assertEqual(3, len(group_component_mappings_set))
        self.assertTrue((ApplicationScreen.delivery, AccessLevel.create))
        self.assertTrue((ApplicationScreen.delivery, AccessLevel.delete))
        self.assertTrue((ApplicationScreen.delivery, AccessLevel.modify))
        group_component_mappings_set = self._test_access_manager_client.get_application_components_accesible_by_group("orphanedGroup")
        self.assertEqual(0, len(group_component_mappings_set))

        user_entity_mappings_set = self._test_access_manager_client.get_entities_accessible_by_user("user5")
        self.assertEqual(3, len(user_entity_mappings_set))
        self.assertTrue((self._CLIENT_ACCOUNTS, self._COMPANY_6) in user_entity_mappings_set)
        self.assertTrue((self._PRODUCT_LINES, self._LINE_7) in user_entity_mappings_set)
        self.assertTrue((self._PRODUCT_LINES, self._LINE_9) in user_entity_mappings_set)
        user_entity_mappings_set = self._test_access_manager_client.get_entities_accessible_by_user("orphanedUser")
        self.assertEqual(0, len(user_entity_mappings_set))

        entities_set: Set[str] = self._test_access_manager_client.get_entities_of_type_accessible_by_user("user5", self._PRODUCT_LINES)
        self.assertEqual(2, len(entities_set))
        self.assertTrue(self._LINE_7 in entities_set)
        self.assertTrue(self._LINE_9 in entities_set)
        entities_set = self._test_access_manager_client.get_entities_of_type_accessible_by_user("orphanedUser", self._PRODUCT_LINES)
        self.assertEqual(0, len(entities_set))

        group_entity_mappings_set: Set[Tuple[str, str]] = self._test_access_manager_client.get_entities_accessible_by_group("group4")
        self.assertEqual(4, len(group_entity_mappings_set))
        self.assertTrue((self._CLIENT_ACCOUNTS, self._COMPANY_1) in group_entity_mappings_set)
        self.assertTrue((self._PRODUCT_LINES, self._LINE_8) in group_entity_mappings_set)
        self.assertTrue((self._PRODUCT_LINES, self._LINE_9) in group_entity_mappings_set)
        self.assertTrue((self._PRODUCT_LINES, self._LINE_10) in group_entity_mappings_set)
        group_entity_mappings_set = self._test_access_manager_client.get_entities_accessible_by_group("orphanedGroup")
        self.assertEqual(0, len(group_entity_mappings_set))

        entities_set = self._test_access_manager_client.get_entities_of_type_accessible_by_group("group4", self._PRODUCT_LINES)
        self.assertEqual(3, len(entities_set))
        self.assertTrue(self._LINE_8 in entities_set)
        self.assertTrue(self._LINE_9 in entities_set)
        self.assertTrue(self._LINE_10 in entities_set)
        entities_set = self._test_access_manager_client.get_entities_of_type_accessible_by_group("orphanedGroup", self._PRODUCT_LINES)
        self.assertEqual(0, len(entities_set))


    def test_remove_elements_and_mappings(self):

        self._test_access_manager_client.remove_group_to_entity_mapping("group6", self._CLIENT_ACCOUNTS, self._COMPANY_1)
        self._test_access_manager_client.remove_group_to_entity_mapping("group6", self._PRODUCT_LINES, self._LINE_10)
        self._test_access_manager_client.remove_group_to_entity_mapping("group5", self._PRODUCT_LINES, self._LINE_9)
        self._test_access_manager_client.remove_group_to_entity_mapping("group4", self._PRODUCT_LINES, self._LINE_8)
        self._test_access_manager_client.remove_group_to_entity_mapping("group3", self._PRODUCT_LINES, self._LINE_7)
        self._test_access_manager_client.remove_group_to_entity_mapping("group2", self._PRODUCT_LINES, self._LINE_6)
        self._test_access_manager_client.remove_group_to_entity_mapping("group1", self._PRODUCT_LINES, self._LINE_5)
        self._test_access_manager_client.remove_group_to_entity_mapping("group1", self._PRODUCT_LINES, self._LINE_4)

        self._test_access_manager_client.remove_user_to_entity_mapping("user12", self._PRODUCT_LINES, self._LINE_3)
        self._test_access_manager_client.remove_user_to_entity_mapping("user11", self._PRODUCT_LINES, self._LINE_2)
        self._test_access_manager_client.remove_user_to_entity_mapping("user10", self._PRODUCT_LINES, self._LINE_1)
        self._test_access_manager_client.remove_user_to_entity_mapping("user9", self._CLIENT_ACCOUNTS, self._COMPANY_10)
        self._test_access_manager_client.remove_user_to_entity_mapping("user8", self._CLIENT_ACCOUNTS, self._COMPANY_9)
        self._test_access_manager_client.remove_user_to_entity_mapping("user7", self._CLIENT_ACCOUNTS, self._COMPANY_8)
        self._test_access_manager_client.remove_user_to_entity_mapping("user6", self._CLIENT_ACCOUNTS, self._COMPANY_7)
        self._test_access_manager_client.remove_user_to_entity_mapping("user5", self._CLIENT_ACCOUNTS, self._COMPANY_6)
        self._test_access_manager_client.remove_user_to_entity_mapping("user4", self._CLIENT_ACCOUNTS, self._COMPANY_5)
        self._test_access_manager_client.remove_user_to_entity_mapping("user3", self._CLIENT_ACCOUNTS, self._COMPANY_4)
        self._test_access_manager_client.remove_user_to_entity_mapping("user2", self._CLIENT_ACCOUNTS, self._COMPANY_3)
        self._test_access_manager_client.remove_user_to_entity_mapping("user1", self._CLIENT_ACCOUNTS, self._COMPANY_2)
        self._test_access_manager_client.remove_user_to_entity_mapping("user1", self._CLIENT_ACCOUNTS, self._COMPANY_1)

        self._test_access_manager_client.remove_group_to_application_component_and_access_level_mapping("group6", ApplicationScreen.delivery, AccessLevel.delete)
        self._test_access_manager_client.remove_group_to_application_component_and_access_level_mapping("group5", ApplicationScreen.delivery, AccessLevel.modify)
        self._test_access_manager_client.remove_group_to_application_component_and_access_level_mapping("group4", ApplicationScreen.delivery, AccessLevel.create)
        self._test_access_manager_client.remove_group_to_application_component_and_access_level_mapping("group3", ApplicationScreen.delivery, AccessLevel.view)
        self._test_access_manager_client.remove_group_to_application_component_and_access_level_mapping("group2", ApplicationScreen.settings, AccessLevel.delete)
        self._test_access_manager_client.remove_group_to_application_component_and_access_level_mapping("group1", ApplicationScreen.settings, AccessLevel.modify)
        self._test_access_manager_client.remove_group_to_application_component_and_access_level_mapping("group1", ApplicationScreen.settings, AccessLevel.create)

        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user12", ApplicationScreen.settings, AccessLevel.view)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user11", ApplicationScreen.manage_products, AccessLevel.delete)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user10", ApplicationScreen.manage_products, AccessLevel.modify)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user9", ApplicationScreen.manage_products, AccessLevel.create)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user8", ApplicationScreen.manage_products, AccessLevel.view)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user7", ApplicationScreen.summary, AccessLevel.delete)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user6", ApplicationScreen.summary, AccessLevel.modify)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user5", ApplicationScreen.summary, AccessLevel.create)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user4", ApplicationScreen.summary, AccessLevel.view)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user3", ApplicationScreen.order, AccessLevel.delete)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user2", ApplicationScreen.order, AccessLevel.modify)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user1", ApplicationScreen.order, AccessLevel.create)
        self._test_access_manager_client.remove_user_to_application_component_and_access_level_mapping("user1", ApplicationScreen.order, AccessLevel.view)

        self._test_access_manager_client.remove_group_to_group_mapping("unmappedGroup1", "unmappedGroup2")
        self._test_access_manager_client.remove_group_to_group_mapping("group4", "group6")
        self._test_access_manager_client.remove_group_to_group_mapping("group4", "group5")
        self._test_access_manager_client.remove_group_to_group_mapping("group3", "group5")
        self._test_access_manager_client.remove_group_to_group_mapping("group2", "group4")
        self._test_access_manager_client.remove_group_to_group_mapping("group1", "group4")
        self._test_access_manager_client.remove_group_to_group_mapping("group1", "group3")

        self._test_access_manager_client.remove_user_to_group_mapping("unmappedUser1", "unmappedGroup1")
        self._test_access_manager_client.remove_user_to_group_mapping("user12", "group6")
        self._test_access_manager_client.remove_user_to_group_mapping("user11", "group6")
        self._test_access_manager_client.remove_user_to_group_mapping("user10", "group5")
        self._test_access_manager_client.remove_user_to_group_mapping("user9", "group5")
        self._test_access_manager_client.remove_user_to_group_mapping("user8", "group4")
        self._test_access_manager_client.remove_user_to_group_mapping("user7", "group4")
        self._test_access_manager_client.remove_user_to_group_mapping("user6", "group3")
        self._test_access_manager_client.remove_user_to_group_mapping("user5", "group3")
        self._test_access_manager_client.remove_user_to_group_mapping("user4", "group2")
        self._test_access_manager_client.remove_user_to_group_mapping("user3", "group2")
        self._test_access_manager_client.remove_user_to_group_mapping("user2", "group1")
        self._test_access_manager_client.remove_user_to_group_mapping("user1", "group1")

        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_10)
        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_9)
        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_8)
        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_7)
        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_6)
        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_5)
        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_4)
        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_3)
        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_2)
        self._test_access_manager_client.remove_entity(self._PRODUCT_LINES, self._LINE_1)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_10)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_9)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_8)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_7)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_6)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_5)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_4)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_3)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_2)
        self._test_access_manager_client.remove_entity(self._CLIENT_ACCOUNTS, self._COMPANY_1)
        self._test_access_manager_client.remove_entity_type(self._UNMAPPED)
        self._test_access_manager_client.remove_entity_type(self._PRODUCT_LINES)
        self._test_access_manager_client.remove_entity_type(self._CLIENT_ACCOUNTS)

        self._test_access_manager_client.remove_group("orphanedGroup")
        self._test_access_manager_client.remove_group("unmappedGroup2")
        self._test_access_manager_client.remove_group("unmappedGroup1")
        self._test_access_manager_client.remove_group("group6")
        self._test_access_manager_client.remove_group("group5")
        self._test_access_manager_client.remove_group("group4")
        self._test_access_manager_client.remove_group("group3")
        self._test_access_manager_client.remove_group("group2")
        self._test_access_manager_client.remove_group("group1")

        self._test_access_manager_client.remove_user("orphanedUser")
        self._test_access_manager_client.remove_user("unmappedUser1")
        self._test_access_manager_client.remove_user("user12")
        self._test_access_manager_client.remove_user("user11")
        self._test_access_manager_client.remove_user("user10")
        self._test_access_manager_client.remove_user("user9")
        self._test_access_manager_client.remove_user("user8")
        self._test_access_manager_client.remove_user("user7")
        self._test_access_manager_client.remove_user("user6")
        self._test_access_manager_client.remove_user("user5")
        self._test_access_manager_client.remove_user("user4")
        self._test_access_manager_client.remove_user("user3")
        self._test_access_manager_client.remove_user("user2")
        self._test_access_manager_client.remove_user("user1")


    #region Inner Classes

    class _ApplicationScreenUniqueStringifier(UniqueStringifierBase[ApplicationScreen]):

        def to_string(self, input_object: ApplicationScreen) -> str:
            if (input_object == ApplicationScreen.order):
                return "Order"
            elif (input_object == ApplicationScreen.summary):
                return "Summary"
            elif (input_object == ApplicationScreen.manage_products):
                return "ManageProducts"
            elif (input_object == ApplicationScreen.settings):
                return "Settings"
            elif (input_object == ApplicationScreen.delivery):
                return "Delivery"
            elif (input_object == ApplicationScreen.review):
                return "Review"
            elif (input_object == ApplicationScreen.reserved_characters):
                return AccessManagerClientIntegrationTests()._URL_RESERVED_CHARACTERS
            else:
                raise ValueError("Unhandled ApplicationScreen value '{0}'.".format(input_object))


        def from_string(self, stringified_object: str) -> ApplicationScreen:
            if (stringified_object == "Order"):
                return ApplicationScreen.order
            elif (stringified_object == "Summary"):
                return ApplicationScreen.summary
            elif (stringified_object == "ManageProducts"):
                return ApplicationScreen.manage_products
            elif (stringified_object == "Settings"):
                return ApplicationScreen.settings
            elif (stringified_object == "Delivery"):
                return ApplicationScreen.delivery
            elif (stringified_object == "Review"):
                return ApplicationScreen.review
            elif (stringified_object == AccessManagerClientIntegrationTests()._URL_RESERVED_CHARACTERS):
                return ApplicationScreen.reserved_characters
            else:
                raise ValueError("Unhandled value '{0}'.".format(stringified_object))


    class _AccessLevelUniqueStringifier(UniqueStringifierBase[AccessLevel]):

        def to_string(self, input_object: AccessLevel) -> str:
            if (input_object == AccessLevel.view):
                return "View"
            elif (input_object == AccessLevel.create):
                return "Create"
            elif (input_object == AccessLevel.modify):
                return "Modify"
            elif (input_object == AccessLevel.delete):
                return "Delete"
            elif (input_object == AccessLevel.reserved_characters):
                return AccessManagerClientIntegrationTests()._URL_RESERVED_CHARACTERS
            else:
                raise ValueError("Unhandled AccessLevel value '{0}'.".format(input_object))


        def from_string(self, stringified_object: str) -> AccessLevel:
            if (stringified_object == "View"):
                return AccessLevel.view
            elif (stringified_object == "Create"):
                return AccessLevel.create
            elif (stringified_object == "Modify"):
                return AccessLevel.modify
            elif (stringified_object == "Delete"):
                return AccessLevel.delete
            elif (stringified_object == AccessManagerClientIntegrationTests()._URL_RESERVED_CHARACTERS):
                return AccessLevel.reserved_characters
            else:
                raise ValueError("Unhandled value '{0}'.".format(stringified_object))

    #endregion

if __name__ == "__main__":
    unittest.main()
