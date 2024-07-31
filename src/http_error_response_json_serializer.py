from typing import Dict, List, Tuple, Any, Union

from models.http_error_response import HttpErrorResponse
from exceptions.deserialization_error import DeserializationError

class HttpErrorResponseJsonSerializer:
    """Serializes and deserializes HttpErrorResponse instances to and from JSON documents."""

    _ERROR_PROPERTY_NAME: str = "error"
    _CODE_PROPERTY_NAME: str = "code"
    _MESSAGE_PROPERTY_NAME: str = "message"
    _TARGET_PROPERTY_NAME: str = "target"
    _ATTRIBUTES_PROPERTY_NAME: str = "attributes"
    _NAME_PROPERTY_NAME: str = "name"
    _VALUE_PROPERTY_NAME: str = "value"
    _INNER_ERROR_PROPERTY_NAME: str = "innererror"

    def serialize(self, http_error_response: HttpErrorResponse) -> Dict[str, Any]:
        """Serializes the specified HttpErrorResponse to a JSON document.
        
        Args:
            http_error_response: 
                The HttpErrorResponse object to serialize.

        Returns:
            A JSON document representing the HttpErrorResponse.
        """
        return_json_dict: Dict[str, Any] = dict()
        return_json_dict[self._ERROR_PROPERTY_NAME] = self.serialize_error(http_error_response)

        return return_json_dict


    def deserialize(self, json_object: Dict[str, Any]) -> HttpErrorResponse:
        """Deserializes the specified JSON object to a HttpErrorResponse object.
        
        Args:
            json_object: 
                The deserialized HttpErrorResponse.

        Returns:
            Failed to deserialize the HttpErrorResponse.

        Raises:
            DeserializationException: Failed to deserialize.
        """
        if (self._ERROR_PROPERTY_NAME in json_object and isinstance(json_object[self._ERROR_PROPERTY_NAME], dict) == True):
            return self.deserialize_error(json_object[self._ERROR_PROPERTY_NAME])
        else:
            raise DeserializationError("Failed to deserialize HttpErrorResponse.  The specified JSON Dict did not contain an '{0}' property.".format(self._ERROR_PROPERTY_NAME))


    def serialize_error(self, http_error_response: HttpErrorResponse) -> Dict[str, Any]:
        """Serializes the 'error' and 'inner_error' properties of the JSON document returned by the serialize() method.
        
        Args:
            http_error_response: 
                The HttpErrorResponse object to serialize.

        Returns:
            The 'error' or 'innererror' property of the JSON document.
        """
        return_json_dict: Dict[str, Any] = dict()

        return_json_dict[self._CODE_PROPERTY_NAME] = http_error_response.code
        return_json_dict[self._MESSAGE_PROPERTY_NAME] = http_error_response.message
        if (http_error_response.target is not None):
            return_json_dict[self._TARGET_PROPERTY_NAME] = http_error_response.target
        attributes_json: List[Dict[str, Any]] = list()
        for current_attribute in http_error_response.attributes:
            current_attribute_json: Dict[str, Any] = dict()
            current_attribute_json[self._NAME_PROPERTY_NAME] = current_attribute[0]
            #print(type(current_attribute[0]))
            current_attribute_json[self._VALUE_PROPERTY_NAME] = current_attribute[1]
            attributes_json.append(current_attribute_json)
        if (len(attributes_json) > 0):
            return_json_dict[self._ATTRIBUTES_PROPERTY_NAME] = attributes_json
        if (http_error_response.inner_error is not None):
            return_json_dict[self._INNER_ERROR_PROPERTY_NAME] = self.serialize_error(http_error_response.inner_error)

        return return_json_dict


    def deserialize_error(self, json_object: Dict[str, Any]) -> HttpErrorResponse:
        """Deserializes the 'error' and 'inner_error' properties of a JSON document containing a serialized HttpErrorResponse.
        
        Args:
            json_object: 
                The 'error' or 'innererror' property of the JSON object to deserialize.

        Returns:
            The deserialized 'error' or 'innererror' property, or null if the property could not be deserialized.

        Raises:
            DeserializationException: Failed to deserialize a property.
        """
        if (self._CODE_PROPERTY_NAME not in json_object):
            raise DeserializationError("Failed to deserialize HttpErrorResponse 'error' or 'innererror' property.  The specified JSON Dict did not contain a '{0}' property.".format(self._CODE_PROPERTY_NAME))
        if (self._MESSAGE_PROPERTY_NAME not in json_object):
            raise DeserializationError("Failed to deserialize HttpErrorResponse 'error' or 'innererror' property.  The specified JSON Dict did not contain a '{0}' property.".format(self._MESSAGE_PROPERTY_NAME))
        
        code: str = json_object[self._CODE_PROPERTY_NAME]
        message: str = json_object[self._MESSAGE_PROPERTY_NAME]
        target: Union[str, None] = None
        attributes: List[Tuple[str, str]] = list()
        inner_error: Union[HttpErrorResponse, None] = None

        # Deserialize optional properties
        if (self._TARGET_PROPERTY_NAME in json_object):
            target = json_object[self._TARGET_PROPERTY_NAME]
            
        if (self._ATTRIBUTES_PROPERTY_NAME in json_object and isinstance(json_object[self._ATTRIBUTES_PROPERTY_NAME], list) == True):
            attributes_json: List[Dict[str, Any]] = json_object[self._ATTRIBUTES_PROPERTY_NAME]
            for current_attribute_json in attributes_json:
                if (self._NAME_PROPERTY_NAME in current_attribute_json and self._VALUE_PROPERTY_NAME in current_attribute_json):
                    attributes.append(( current_attribute_json[self._NAME_PROPERTY_NAME], current_attribute_json[self._VALUE_PROPERTY_NAME] ))

        if (self._INNER_ERROR_PROPERTY_NAME in json_object and isinstance(json_object[self._INNER_ERROR_PROPERTY_NAME], dict) == True):
            inner_error = self.deserialize_error(json_object[self._INNER_ERROR_PROPERTY_NAME])

        return HttpErrorResponse(code, message, target, attributes, inner_error)
