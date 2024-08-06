from typing import List, Dict, TypeVar, Tuple, Iterable, Any, Union
from unique_stringifier_base import UniqueStringifierBase

T1 = TypeVar("T1")
T2 = TypeVar("T2")

class JsonArrayToIterableConverter():
    """Converts Lists containing JSON arrays (i.e. created by json.loads()) to Iterable instances.
    """

    def convert_to_iterable_of_tuples(
        self, 
        input_dicts: List[Dict[str, Any]], 
        key_1: str, 
        key_2: str, 
        stringifier_1: UniqueStringifierBase[T1], 
        stringifier_2: UniqueStringifierBase[T2], 
    ) -> Iterable[Tuple[T1, T2]]:
        """Converts an array of JSON objects (i.e. created by json.loads()) to an iterable of tuples of 2 values.

        Args:
            input_dicts:
                List representing an array of JSON objects (represented as Dicts) to convert.
            key_1:
                The name of the first JSON property (of each array element) to convert.
            key_2:
                The name of the second JSON property (of each array element) to convert.
            stringifier_1:
                UniqueStringifierBase instance to use to convert the first JSON property (of each array element) value to type T1.
            stringifier_2:
                UniqueStringifierBase instance to use to convert the second JSON property (of each array element) value to type T2.

        Returns:
            An iterable of tuples of 2 values of types T1 and T2 respectively.
        """
        if (isinstance(input_dicts, List) == False):
            raise ValueError("Parameter 'input_dicts' was expected to be of type '{0}' but was '{1}'.".format(type(list()), type(input_dicts)))
        
        for current_element in input_dicts:
            if (isinstance(current_element, Dict) == False):
                raise ValueError("Element of parameter 'input_dicts' was expected to be of type '{0}' but was '{1}'.".format(type(dict()), type(current_element)))
            self._raise_error_if_key_not_in_dict(current_element, key_1, "input_dicts")
            self._raise_error_if_key_not_in_dict(current_element, key_2, "input_dicts")
            self._raise_error_if_dict_value_not_of_type(current_element, key_1, str, "input_dicts")
            self._raise_error_if_dict_value_not_of_type(current_element, key_2, str, "input_dicts")
            converted_value_1: T1 = stringifier_1.from_string(current_element[key_1])
            converted_value_2: T2 = stringifier_2.from_string(current_element[key_2])

            yield ( converted_value_1, converted_value_2 )


    def convert_to_iterable(self, input_list: Union[List[str], List[Dict[str, Any]]] , stringifier: UniqueStringifierBase[T1], key: Union[str, None] = None) -> Iterable[T1]:
        """Converts an array of either JSON strings or objects (i.e. created by json.loads()) to an iterable of single values.

        Args:
            input_list:
                List representing an array of either JSON strings or objects to convert.
            stringifier:
                UniqueStringifierBase instance to use to convert each element of the array (in the case of a string array), or convert the value of the property specified in parameter 'key' (in the case of an object array) to type T1.
            key:
                Optional name of the JSON property (of each array element) to convert, for the case that parameter 'input_list' is a List of Dicts (i.e. of JSON objects).  Should be set to None if parameter 'input_list' is a List of strings.

        Returns:
            An iterable of single values of type T1.
        """
        if (isinstance(input_list, List) == False):
            raise ValueError("Parameter 'input_list' was expected to be of type '{0}' but was '{1}'.".format(type(list()), type(input_list)))
        
        encountered_first_value: bool = False
        array_elements_are_strings: bool = True
        for current_element in input_list:
            if (encountered_first_value == False):
                if (not( (isinstance(current_element, str) == True) or (isinstance(current_element, dict) == True) )):
                    raise ValueError("Element of list parameter 'input_list' was expected to be of type '{0}' or '{1}' but was '{2}'.".format(type(""), type(dict()), type(current_element)))
                if (isinstance(current_element, dict) == True):
                    array_elements_are_strings = False
                if (array_elements_are_strings == False and key is None):
                    raise ValueError("Parameter 'input_list' contains '{0}' elements, but parameter 'key' was not specified.".format(type(dict())))
                if (array_elements_are_strings == True and key is not None):
                    raise ValueError("Parameter 'input_list' contains '{0}' elements, but parameter 'key' was specified.".format(type("")))
                encountered_first_value = True

            if (array_elements_are_strings == True):
                if (isinstance(current_element, str) == False):
                    raise ValueError("Parameter 'input_list' was expected to contain '{0}' elements, but '{1}' element was encountered.".format(type(""), type(current_element)))
                assert isinstance(current_element, str)
                converted_value: T1 = stringifier.from_string(current_element)

            else:
                if (isinstance(current_element, dict) == False):
                    raise ValueError("Parameter 'input_list' was expected to contain '{0}' elements, but '{1}' element was encountered.".format(type(dict()), type(current_element)))
                assert isinstance(current_element, dict)
                assert isinstance(key, str)
                converted_value: T1 = stringifier.from_string(current_element[key])

            yield converted_value


    #region Private/Protected Methods

    def _raise_error_if_key_not_in_dict(self, input_dict: Dict[str, Any], key: str, parameter_name: str) -> None:
        if (key not in input_dict):
            raise ValueError("Element of dict parameter '{0}' does not contain key '{1}'.".format(parameter_name, key))
        
    
    def _raise_error_if_dict_value_not_of_type(self, input_dict: Dict[str, Any], key: str, expected_type: type, parameter_name: str) -> None:
        if (isinstance(input_dict[key], expected_type) == False):
            raise ValueError("Value of key '{0}' of element of dict parameter '{1}' was expected to be of type '{2}' but was '{3}'.".format(
                key, 
                parameter_name, 
                expected_type, 
                type(input_dict[key])
                )
            )

    #endregion