from typing import Dict, List, Tuple
import json
import unittest

from models.http_error_response import HttpErrorResponse
from exceptions.deserialization_error import DeserializationError
from http_error_response_json_serializer import HttpErrorResponseJsonSerializer

class HttpErrorResponseJsonSerializerUnitTests(unittest.TestCase):
    """Unit tests for the HttpErrorResponseJsonSerializer class."""

    def setUp(self):
        self._test_http_error_response_json_serializer = HttpErrorResponseJsonSerializer()


    def test_serialize_http_error_response_with_code_and_message(self):
        error_response = HttpErrorResponse(
            "ArgumentException", 
            "Argument 'recordCount' must be greater than or equal to 0."
        )
        expected_json_string = """
            {
                "error" : {
                    "code" : "ArgumentException", 
                    "message" : "Argument 'recordCount' must be greater than or equal to 0."
                }
            }
        """
        expected_json = json.loads(expected_json_string)

        result: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(error_response)

        self.assertEqual(expected_json, result)


    def test_serialize_http_error_response_with_code_message_and_target(self):
        error_response = HttpErrorResponse(
            "ArgumentException", 
            "Argument 'recordCount' must be greater than or equal to 0.", 
            "recordCount"
        )
        expected_json_string = """
            {
                "error" : {
                    "code" : "ArgumentException", 
                    "message" : "Argument 'recordCount' must be greater than or equal to 0.", 
                    "target" : "recordCount"
                }
            }
        """
        expected_json = json.loads(expected_json_string)

        result: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(error_response)

        self.assertEqual(expected_json, result)


    def test_serialize_http_error_response_with_code_message_and_attributes(self):
        error_response = HttpErrorResponse(
            "ArgumentException", 
            "A mapping between user 'user1' and group 'group1' already exists.", 
            attributes=[  
                ("user", "user1"), 
                ("group", "group1")
            ]
        )
        expected_json_string = """
        {
            "error" : {
                "code" : "ArgumentException", 
                "message" : "A mapping between user 'user1' and group 'group1' already exists.", 
                "attributes" : 
                [
                    { "name": "user", "value": "user1" }, 
                    { "name": "group", "value": "group1" }
                ]
            }
        }
        """
        expected_json = json.loads(expected_json_string)

        result: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(error_response)

        self.assertEqual(expected_json, result)

    
    def test_serialize_http_error_response_with_code_message_and_inner_error(self):
        error_response = HttpErrorResponse(
            "ArgumentException", 
            "A mapping between user 'user1' and group 'group1' already exists.", 
            inner_error=HttpErrorResponse(
                "ArgumentException", 
                "An edge already exists between vertices 'child' and 'parent'."
            )
        )
        expected_json_string = """
        {
            "error" : {
                "code" : "ArgumentException", 
                "message" : "A mapping between user 'user1' and group 'group1' already exists.", 
                "innererror" : 
                {
                    "code" : "ArgumentException", 
                    "message" : "An edge already exists between vertices 'child' and 'parent'."
                }
            }
        }
        """
        expected_json = json.loads(expected_json_string)

        result: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(error_response)

        self.assertEqual(expected_json, result)


    def test_serialize_http_error_response_with_all_properties(self):
        error_response = HttpErrorResponse(
            "ArgumentException", 
            "Failed to add edge to graph.",
            target="graph",
            attributes=[  
                ("fromVertex", "child"), 
                ("toVertex", "parent")
            ], 
            inner_error=HttpErrorResponse(
                "ArgumentException", 
                "An edge already exists between vertices 'child' and 'parent'."
            )
        )
        expected_json_string = """
        {
            "error" : {
                "code" : "ArgumentException", 
                "message" : "Failed to add edge to graph.", 
                "target" : "graph", 
                "attributes" : 
                [
                    { "name": "fromVertex", "value": "child" }, 
                    { "name": "toVertex", "value": "parent" }
                ], 
                "innererror" : 
                {
                    "code" : "ArgumentException", 
                    "message" : "An edge already exists between vertices 'child' and 'parent'." 
                }
            }
        }
        """
        expected_json = json.loads(expected_json_string)

        result: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(error_response)

        self.assertEqual(expected_json, result)


    def test_deserialize_json_doesnt_contain_error_property(self):
        with self.assertRaises(DeserializationError) as result:
            self._test_http_error_response_json_serializer.deserialize(dict())

        self.assertEqual("Failed to deserialize HttpErrorResponse.  The specified JSON Dict did not contain an 'error' property.", str(result.exception))


    def test_deserialize_error_property_not_dict(self):
        test_json_object = { "error": list() } 

        with self.assertRaises(DeserializationError) as result:
            self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual("Failed to deserialize HttpErrorResponse.  The specified JSON Dict did not contain an 'error' property.", str(result.exception))


    def tests_deserialize_error_object_doesnt_contain_code_property(self):
        test_json_object = json.loads("""
        {
            "error" : {
                "message" : "Failed to add edge to graph."
            }
        }
        """)

        with self.assertRaises(DeserializationError) as result:
            self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual("Failed to deserialize HttpErrorResponse 'error' or 'innererror' property.  The specified JSON Dict did not contain a 'code' property.", str(result.exception))


    def tests_deserialize_error_object_doesnt_contain_message_property(self):
        test_json_object = json.loads("""
        {
            "error" : {
                "code" : "ArgumentException"
            }
        }
        """)

        with self.assertRaises(DeserializationError) as result:
            self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual("Failed to deserialize HttpErrorResponse 'error' or 'innererror' property.  The specified JSON Dict did not contain a 'message' property.", str(result.exception))


    def tests_deserialize_no_inner_error(self):
        test_code: str = "ArgumentException"
        test_message: str = "Failed to add edge to graph."
        test_target: str = "graph"
        test_attributes: List[Tuple[str, str]] = [  
            ("fromVertex", "child"), 
            ("toVertex", "parent")
        ]
        test_error_response = HttpErrorResponse(test_code, test_message, test_target, test_attributes)
        test_json_object: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(test_error_response)

        result: HttpErrorResponse = self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual(test_code, result.code)
        self.assertEqual(test_message, result.message)
        self.assertEqual(test_target, result.target)
        self.assertEqual(test_attributes[0], result.attributes[0])
        self.assertEqual(test_attributes[1], result.attributes[1])
        self.assertIsNone(result.inner_error)


        test_error_response = HttpErrorResponse(test_code, test_message, test_target)
        test_json_object: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(test_error_response)

        result = self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual(test_code, result.code)
        self.assertEqual(test_message, result.message)
        self.assertEqual(test_target, result.target)
        self.assertEqual(0, len(result.attributes))
        self.assertIsNone(result.inner_error)


        test_error_response = HttpErrorResponse(test_code, test_message, attributes=test_attributes)
        test_json_object: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(test_error_response)

        result = self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual(test_code, result.code)
        self.assertEqual(test_message, result.message)
        self.assertIsNone(result.target)
        self.assertEqual(test_attributes[0], result.attributes[0])
        self.assertEqual(test_attributes[1], result.attributes[1])
        self.assertIsNone(result.inner_error)


        test_error_response = HttpErrorResponse(test_code, test_message)
        test_json_object: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(test_error_response)

        result = self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual(test_code, result.code)
        self.assertEqual(test_message, result.message)
        self.assertIsNone(result.target)
        self.assertEqual(0, len(result.attributes))
        self.assertIsNone(result.inner_error)
        

    def test_deserialize_including_inner_error(self):
        test_code: str = "ArgumentException"
        test_message: str = "Failed to add edge to graph."
        test_target: str = "graph"
        test_attributes: List[Tuple[str, str]] = [  
            ("fromVertex", "child"), 
            ("toVertex", "parent")
        ]
        test_inner_error_code: str = "Exception"
        test_inner_error_message: str = "An edge already exists between vertices 'child' and 'parent'."
        test_inner_error = HttpErrorResponse(test_inner_error_code, test_inner_error_message)
        test_error_response = HttpErrorResponse(test_code, test_message, test_target, test_attributes, test_inner_error)
        test_json_object: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(test_error_response)

        result: HttpErrorResponse = self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual(test_code, result.code)
        self.assertEqual(test_message, result.message)
        self.assertEqual(test_target, result.target)
        self.assertEqual(test_attributes[0], result.attributes[0])
        self.assertEqual(test_attributes[1], result.attributes[1])
        self.assertIsNotNone(result.inner_error)
        self.assertEqual(test_inner_error_code, result.inner_error.code)
        self.assertEqual(test_inner_error_message, result.inner_error.message)


        test_error_response = HttpErrorResponse(test_code, test_message, test_target, inner_error=test_inner_error)
        test_json_object: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(test_error_response)

        result: HttpErrorResponse = self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual(test_code, result.code)
        self.assertEqual(test_message, result.message)
        self.assertEqual(test_target, result.target)
        self.assertEqual(0, len(result.attributes))
        self.assertIsNotNone(result.inner_error)
        self.assertEqual(test_inner_error_code, result.inner_error.code)
        self.assertEqual(test_inner_error_message, result.inner_error.message)


        test_error_response = HttpErrorResponse(test_code, test_message, attributes=test_attributes, inner_error=test_inner_error)
        test_json_object: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(test_error_response)

        result: HttpErrorResponse = self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual(test_code, result.code)
        self.assertEqual(test_message, result.message)
        self.assertIsNone(result.target)
        self.assertEqual(test_attributes[0], result.attributes[0])
        self.assertEqual(test_attributes[1], result.attributes[1])
        self.assertIsNotNone(result.inner_error)
        self.assertEqual(test_inner_error_code, result.inner_error.code)
        self.assertEqual(test_inner_error_message, result.inner_error.message)


        test_error_response = HttpErrorResponse(test_code, test_message, inner_error=test_inner_error)
        test_json_object: Dict[str, object] = self._test_http_error_response_json_serializer.serialize(test_error_response)

        result: HttpErrorResponse = self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual(test_code, result.code)
        self.assertEqual(test_message, result.message)
        self.assertIsNone(result.target)
        self.assertEqual(0, len(result.attributes))
        self.assertIsNotNone(result.inner_error)
        self.assertEqual(test_inner_error_code, result.inner_error.code)
        self.assertEqual(test_inner_error_message, result.inner_error.message)


    def test_deserialize_multi_level_inner_errors(self):
        test_json_object = json.loads("""
        {
            "error": {
                "code": "BufferFlushingException",
                "message": "Exception occurred on buffer flushing worker thread at 2023-01-29 12:29:12.075 +09:00.",
                "target": "Throw",
                "innererror": {
                    "code": "Exception",
                    "message": "Failed to process buffers and persist flushed events.",
                    "target": "Flush",
                    "innererror": {
                        "code": "Exception",
                        "message": "Failed to execute stored procedure 'ProcessEvents' in SQL Server.",
                        "target": "ExecuteStoredProcedure"
                    }
                }
            }
        }
        """)

        result: HttpErrorResponse = self._test_http_error_response_json_serializer.deserialize(test_json_object)

        self.assertEqual("BufferFlushingException", result.code)
        self.assertEqual("Exception occurred on buffer flushing worker thread at 2023-01-29 12:29:12.075 +09:00.", result.message)
        self.assertEqual("Throw", result.target)
        self.assertEqual("Exception", result.inner_error.code)
        self.assertEqual("Failed to process buffers and persist flushed events.", result.inner_error.message)
        self.assertEqual("Flush", result.inner_error.target)
        self.assertEqual("Exception", result.inner_error.inner_error.code)
        self.assertEqual("Failed to execute stored procedure 'ProcessEvents' in SQL Server.", result.inner_error.inner_error.message)
        self.assertEqual("ExecuteStoredProcedure", result.inner_error.inner_error.target)


if __name__ == "__main__":
    unittest.main()
