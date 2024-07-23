from typing import List, Dict, TypeVar, Set, Tuple, Iterable
from unique_stringifier_base import UniqueStringifierBase

T1 = TypeVar("T1")
T2 = TypeVar("T2")

class JsonDictToContainerConverter():
    """Converts a Dict containing JSON (e.g. created by json.loads()) to Python 'container' datatype or Iterable.
    """

    def convert_to_iterable_of_tuples(
        self, 
        input_dicts: List[Dict[str, str]], 
        key_1: str, 
        key_2: str, 
        stringifier_1: UniqueStringifierBase[T1], 
        stringifier_2: UniqueStringifierBase[T2], 
    ) -> Iterable[Tuple[T1, T2]]:
        """Converts a Dict containing JSON (e.g. created by json.loads()) to an iterable of tuples of 2 values.

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


    def convert_to_iterable(self, input_list: List[str], stringifier: UniqueStringifierBase[T1]) -> Iterable[T1]:
        """Converts a List containing JSON (e.g. created by json.loads()) to an iterable of single values.

        Args:
            input_list:
                List representing an array of JSON values to convert.
            stringifier:
                UniqueStringifierBase instance to use to convert each element of the array to type T1.

        Returns:
            An iterable of single values of type T1.
        """
        if (isinstance(input_list, List) == False):
            raise ValueError("Parameter 'input_list' was expected to be of type '{0}' but was '{1}'.".format(type(list()), type(input_list)))
        
        for current_element in input_list:
            if (isinstance(current_element, str) == False):
                raise ValueError("Element of list parameter 'input_list' was expected to be of type '{0}' but was '{1}'.".format(type(""), type(current_element)))
            converted_value: T1 = stringifier.from_string(current_element)

            yield converted_value


    def convert_to_set_of_tuples(
        self, 
        input_dicts: List[Dict[str, str]], 
        key_1: str, 
        key_2: str, 
        stringifier_1: UniqueStringifierBase[T1], 
        stringifier_2: UniqueStringifierBase[T2], 
    ) -> Set[Tuple[T1, T2]]:
        """Converts a Dict containing JSON (e.g. created by json.loads()) to a set of tuples of 2 values.

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
            A set of tuples of 2 values of types T1 and T2 respectively.
        """
        return set(self.convert_to_iterable_of_tuples(input_dicts, key_1, key_2, stringifier_1, stringifier_2))


    def convert_to_set(self, input_list: List[str], stringifier: UniqueStringifierBase[T1]) -> Set[T1]:
        """Converts a List containing JSON (e.g. created by json.loads()) to a set of single values.

        Args:
            input_list:
                List representing an array of JSON values to convert.
            stringifier:
                UniqueStringifierBase instance to use to convert each element of the array to type T1.

        Returns:
            A set of single values of type T1.
        """
        return set(self.convert_to_iterable(input_list, stringifier))


    #region Private/Protected Methods

    def _raise_error_if_key_not_in_dict(self, input_dict: Dict[str, object], key: str, parameter_name: str) -> None:
        if (key not in input_dict):
            raise ValueError("Element of dict parameter '{0}' does not contain key '{1}'.".format(parameter_name, key))
        
    
    def _raise_error_if_dict_value_not_of_type(self, input_dict: Dict[str, object], key: str, expected_type: TypeVar, parameter_name: str) -> None:
        if (isinstance(input_dict[key], expected_type) == False):
            raise ValueError("Value of key '{0}' of element of dict parameter '{1}' was expected to be of type '{2}' but was '{3}'.".format(
                key, 
                parameter_name, 
                expected_type, 
                type(input_dict[key])
                )
            )

    #endregion