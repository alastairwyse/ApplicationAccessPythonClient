from typing import List
import unittest

from application_screen import ApplicationScreen
from access_level import AccessLevel
from exceptions.element_not_found_error import ElementNotFoundError
from unique_stringifier_base import UniqueStringifierBase
from string_unique_stringifier import StringUniqueStringifier
from access_manager_client import AccessManagerClient

class AccessManagerClientIntegrationTests(unittest.TestCase):
    """Integration tests for the AccessManagerClient class."""

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

    
    def test_connetion_exceptions(self):

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
            else:
                raise ValueError("Unhandled value '{0}'.".format(stringified_object))

    #endregion

if __name__ == "__main__":
    unittest.main()
