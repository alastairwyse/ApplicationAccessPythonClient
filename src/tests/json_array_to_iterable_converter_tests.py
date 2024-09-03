from typing import List, Tuple, Set
import unittest

from string_unique_stringifier import StringUniqueStringifier
from counting_string_unique_stringifier import CountingStringUniqueStringifier
from src.json_array_to_iterable_converter import JsonArrayToIterableConverter

class JsonDictToIterableConverterTests(unittest.TestCase):
    """Unit tests for the JsonDictToIterableConverter class."""

    def setUp(self):
        self._test_json_dict_to_iterable_converter = JsonArrayToIterableConverter()


    def test_convert_to_iterable_input_list_parameter_not_List(self):
        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable(set(), StringUniqueStringifier())) # type: ignore[assignment]

        self.assertEqual("Parameter 'input_list' was expected to be of type '{0}' but was '{1}'.".format(list, set), str(result.exception))


    def test_convert_to_iterable_first_input_list_element_not_string_nor_dict(self):
        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable([ 1, 2, 3  ], StringUniqueStringifier())) # type: ignore[assignment]

        self.assertEqual("Element of list parameter 'input_list' was expected to be of type '{0}' or '{1}' but was '{2}'.".format(str, dict, int), str(result.exception))


    def test_convert_to_iterable_dict_input_list_key_parameter_none(self):
        test_input_list = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "View" }, 
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]
        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable(test_input_list, StringUniqueStringifier())) 

        self.assertEqual("Parameter 'input_list' contains '{0}' elements, but parameter 'key' was not specified.".format(dict), str(result.exception))


    def test_convert_to_iterable_str_input_list_key_parameter_not_none(self):
        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable([ "User1", "User2", "User3" ], StringUniqueStringifier(), "propertyName")) 

        self.assertEqual("Parameter 'input_list' contains '{0}' elements, but parameter 'key' was specified.".format(str), str(result.exception))


    def test_convert_to_iterable_string_input_list_element_not_string(self):
        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable([ "ABC", 1, "DEF"  ], StringUniqueStringifier())) # type: ignore[assignment]

        self.assertEqual("Parameter 'input_list' was expected to contain '{0}' elements, but '{1}' element was encountered.".format(str, int), str(result.exception))


    def test_convert_to_iterable_dict_input_list_element_not_dict(self):
        test_input_list = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            1,
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]

        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable(test_input_list, StringUniqueStringifier(), "ApplicationComponent")) 

        self.assertEqual("Parameter 'input_list' was expected to contain '{0}' elements, but '{1}' element was encountered.".format(dict, int), str(result.exception))


    def test_convert_to_iterable_dict_input_list_element_does_not_contain_key(self):
        test_input_list = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            { "ApplicationComponent": "SummaryScreen" }, 
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]

        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable(test_input_list, StringUniqueStringifier(), "AccessLevel")) 

        self.assertEqual("Element of parameter 'input_list' does not contain key 'AccessLevel'.", str(result.exception))


    def test_convert_to_iterable_dict_input_list_element_key_value_not_string(self):
        test_input_list = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            { "ApplicationComponent": 1, "AccessLevel": "View" }, 
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]

        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable(test_input_list, StringUniqueStringifier(), "ApplicationComponent")) 

        self.assertEqual("Value of key 'ApplicationComponent' of element of parameter 'input_list' was expected to be of type '{0}' but was '{1}'.".format(str, int), str(result.exception))


    def test_convert_to_iterable_string_input_list(self):
        test_input_list = [ "User1", "User2", "User3" ]
        test_stringifier = CountingStringUniqueStringifier()

        result: List[str] = list(self._test_json_dict_to_iterable_converter.convert_to_iterable(test_input_list, test_stringifier))

        self.assertEqual(3, len(result))
        self.assertEqual("User1", result[0])
        self.assertEqual("User2", result[1])
        self.assertEqual("User3", result[2])
        self.assertEqual(0, test_stringifier._to_string_count)
        self.assertEqual(3, test_stringifier._from_string_count)


    def test_convert_to_iterable_dict_input_list(self):
        test_input_dicts = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            { "ApplicationComponent": "SummaryScreen", "AccessLevel": "View" },
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]
        test_stringifier = CountingStringUniqueStringifier()

        result: List[str] = list(self._test_json_dict_to_iterable_converter.convert_to_iterable(test_input_dicts, test_stringifier, "AccessLevel"))

        self.assertEqual(3, len(result))
        self.assertEqual("Modify", result[0])
        self.assertEqual("View", result[1])
        self.assertEqual("Create", result[2])
        self.assertEqual(0, test_stringifier._to_string_count)
        self.assertEqual(3, test_stringifier._from_string_count)


    def test_convert_to_iterable_of_tuples_input_dicts_parameter_not_List(self):
        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable_of_tuples(
                set(), # type: ignore[assignment]
                "ApplicationComponent", 
                "AccessLevel",
                StringUniqueStringifier(), 
                StringUniqueStringifier()
            ))

        self.assertEqual("Parameter 'input_dicts' was expected to be of type '{0}' but was '{1}'.".format(list, set), str(result.exception))


    def test_convert_to_iterable_of_tuples_input_dicts_element_not_dict(self):
        test_input_dicts = [ set() ]

        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable_of_tuples(
                test_input_dicts, # type: ignore[assignment]
                "ApplicationComponent", 
                "AccessLevel",
                StringUniqueStringifier(), 
                StringUniqueStringifier()
            ))

        self.assertEqual("Element of parameter 'input_dicts' was expected to be of type '{0}' but was '{1}'.".format(dict, set), str(result.exception))


    def test_convert_to_iterable_of_tuples_input_dicts_element_does_not_contain_key_1(self):
        test_input_dicts = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            { "AccessLevel": "View" },
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]

        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable_of_tuples(
                test_input_dicts, 
                "ApplicationComponent", 
                "AccessLevel",
                StringUniqueStringifier(), 
                StringUniqueStringifier()
            ))

        self.assertEqual("Element of parameter 'input_dicts' does not contain key 'ApplicationComponent'.", str(result.exception))


    def test_convert_to_iterable_of_tuples_input_dicts_element_does_not_contain_key_3(self):
        test_input_dicts = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            { "ApplicationComponent": "SummaryScreen" },
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]

        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable_of_tuples(
                test_input_dicts, 
                "ApplicationComponent", 
                "AccessLevel",
                StringUniqueStringifier(), 
                StringUniqueStringifier()
            ))

        self.assertEqual("Element of parameter 'input_dicts' does not contain key 'AccessLevel'.", str(result.exception))


    def test_convert_to_iterable_of_tuples_input_dicts_element_key_1_value_not_string(self):
        test_input_dicts = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            { "ApplicationComponent": 1, "AccessLevel": "View" },
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]

        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable_of_tuples(
                test_input_dicts, 
                "ApplicationComponent", 
                "AccessLevel",
                StringUniqueStringifier(), 
                StringUniqueStringifier()
            ))

        self.assertEqual("Value of key 'ApplicationComponent' of element of parameter 'input_dicts' was expected to be of type '{0}' but was '{1}'.".format(str, int), str(result.exception))


    def test_convert_to_iterable_of_tuples_input_dicts_element_key_3_value_not_string(self):
        test_input_dicts = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            { "ApplicationComponent": "SummaryScreen", "AccessLevel": 1 },
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]

        with self.assertRaises(ValueError) as result:
            list(self._test_json_dict_to_iterable_converter.convert_to_iterable_of_tuples(
                test_input_dicts, 
                "ApplicationComponent", 
                "AccessLevel",
                StringUniqueStringifier(), 
                StringUniqueStringifier()
            ))

        self.assertEqual("Value of key 'AccessLevel' of element of parameter 'input_dicts' was expected to be of type '{0}' but was '{1}'.".format(str, int), str(result.exception))


    def test_convert_to_iterable_of_tuples(self):
        test_input_dicts = [ 
            { "ApplicationComponent": "OrderScreen", "AccessLevel": "Modify" }, 
            { "ApplicationComponent": "SummaryScreen", "AccessLevel": "View" },
            { "ApplicationComponent": "SetupScreen", "AccessLevel": "Create" }
        ]
        test_stringifier_1 = CountingStringUniqueStringifier()
        test_stringifier_2 = CountingStringUniqueStringifier()

        result: List[Tuple[str, str]] = list(self._test_json_dict_to_iterable_converter.convert_to_iterable_of_tuples(
                test_input_dicts, 
                "ApplicationComponent", 
                "AccessLevel",
                test_stringifier_1, 
                test_stringifier_2
            ))

        self.assertEqual(3, len(result))
        self.assertEqual("OrderScreen", result[0][0])
        self.assertEqual("Modify", result[0][1])
        self.assertEqual("SummaryScreen", result[1][0])
        self.assertEqual("View", result[1][1])
        self.assertEqual("SetupScreen", result[2][0])
        self.assertEqual("Create", result[2][1])
        self.assertEqual(0, test_stringifier_1._to_string_count)
        self.assertEqual(3, test_stringifier_1._from_string_count)
        self.assertEqual(0, test_stringifier_2._to_string_count)
        self.assertEqual(3, test_stringifier_2._from_string_count)


if __name__ == "__main__":
    unittest.main()
