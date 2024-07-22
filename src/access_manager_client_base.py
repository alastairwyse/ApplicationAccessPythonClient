from typing import TypeVar, Generic, Dict, Callable
from abc import ABC
import json
from http import HTTPStatus
import requests
from requests import Request

from exceptions.deserialization_error import DeserializationError
from exceptions.not_found_error import NotFoundError
from exceptions.element_not_found_error import ElementNotFoundError
from http_method import HTTPMethod
from http_error_response_json_serializer import HttpErrorResponseJsonSerializer
from models.http_error_response import HttpErrorResponse
from string_unique_stringifier import StringUniqueStringifier
from unique_stringifier_base import UniqueStringifierBase

TUser = TypeVar("TUser")
TGroup = TypeVar("TGroup")
TComponent = TypeVar("TComponent")
TAccess = TypeVar("TAccess")

# TODO:
#   Add constructor params from requests.request, e.g...
#     headers
#     cookies?
#     auth (what is this)
#     timeout
#     proxies
#     verify
#     cert

class AccessManagerClientBase(Generic[TUser, TGroup, TComponent, TAccess], ABC):
    """Base for client classes which interface to AccessManager instances hosted as REST web APIs.

    Generic Paramters:
        TUser:
            The type of users in the AccessManager.
        TGroup:
            The type of groups in the AccessManager.
        TComponent:
            The type of components in the AccessManager.
        TAccess:
            The type of levels of access which can be assigned to an application component.
    
    """

    def __init__(
            self,
            base_url: str, 
            user_stringifier: UniqueStringifierBase=StringUniqueStringifier, 
            group_stringifier: UniqueStringifierBase=StringUniqueStringifier, 
            application_component_stringifier: UniqueStringifierBase=StringUniqueStringifier, 
            access_level_stringifier: UniqueStringifierBase=StringUniqueStringifier, 
        ) -> None:
        """Initialises a new instance of the AccessManagerClientBase class.
        
        Args:
            base_url:
                The base URL for the hosted Web API (must include a trailing forward slash).
            user_stringifier:
                A string converter for users.  Used to convert strings sent to and received from the web API from/to TUser instances.
            group_stringifier:
                A string converter for groups.  Used to convert strings sent to and received from the web API from/to TGroup instances.
            application_component_stringifier:
                A string converter for application components.  Used to convert strings sent to and received from the web API from/to TComponent instances.
            access_level_stringifier:
                A string converter for access levels.  Used to convert strings sent to and received from the web API from/to TAccess instances.
        """
        if (base_url[len(base_url) - 1] != "/"):
            raise ValueError("Parameter 'base_url' with value '{0}' must have a trailing forward slash character.".format(base_url))

        self._error_response_deserializer = HttpErrorResponseJsonSerializer()
        self._initialize_base_url(base_url)
        self._user_stringifier = user_stringifier
        self._group_stringifier = group_stringifier
        self._application_component_stringifier = application_component_stringifier
        self._access_level_stringifier = access_level_stringifier
        self._request_accept_header: Dict[str, str] = { "Accept": "application/json" }


    #region Private/Protected Methods

    # TODO: SendGetRequest()... need to setup generic method.

    def _initialize_base_url(self, base_url: str) -> None:
        """Adds an appropriate path suffix to the specified 'base_url' constructor parameter.

        Args:
            base_url:
                The base URL to initialize.
        """
        self._base_url: str = base_url + "api/v1/"


    def _initialize_status_code_to_exception_throwing_action_map(self) -> None:
        """Initializes the '_status_code_to_exception_throwing_action_map' member.
        """
        self._status_code_to_exception_throwing_action_map: Dict[HTTPStatus, Callable[[HttpErrorResponse]]] = dict()
        self._status_code_to_exception_throwing_action_map[HTTPStatus.INTERNAL_SERVER_ERROR] = self._internal_server_error_exception_throwing_action
        self._status_code_to_exception_throwing_action_map[HTTPStatus.BAD_REQUEST] = self._bad_request_exception_throwing_action
        self._status_code_to_exception_throwing_action_map[HTTPStatus.NOT_FOUND] = self._not_found_exception_throwing_action


    def _handle_non_success_response_status(self, http_method: HTTPMethod, request_url: str, response_status: HTTPStatus, response_body: str):
        """Handles receipt of a non-success HTTP response status, by converting the status and response body to an appropriate Exception and throwing that Exception.

        Args:
            http_method:
                The HTTP method used in the request which generated the response.
            request_url:
                The URL of the request which generated the response.
            response_status:
                The received HTTP response status.
            response_body:
                The received response body.
        """
        base_exception_message: str = "Failed to call URL '{0}' with '{1}' method.  Received non-succces HTTP response status '{2}'".format(
            request_url, 
            http_method, 
            response_status
        )

        # Attempt to deserialize a HttpErrorResponse from the body
        http_error_response: HttpErrorResponse = self._deserialize_response_body_to_http_error_response(response_body)
        if (http_error_response is not None):
            if (response_status in self._status_code_to_exception_throwing_action_map):
                self._status_code_to_exception_throwing_action_map[response_status](http_error_response)
            else:
                exception_message_postfix: str = ", error code '{0}', and error message '{1}'.".format(
                    http_error_response.code, 
                    http_error_response.message
                )
                raise RuntimeError(base_exception_message + exception_message_postfix)
        else:
            if (response_body.isspace() == False):
                raise RuntimeError(base_exception_message + " and response body '{0}'.".format(response_body))
            else:
                raise RuntimeError(base_exception_message + ".")


    def _deserialize_response_body_to_http_error_response(self, response_body: str) -> HttpErrorResponse:
        """Attempts to deserialize the body of a HTTP response received as a string to an HttpErrorResponse instance.

        Args:
            response_body:
                The response body to deserialize.
        Returns:
            The deserialized response body, or null if the reponse could not be deserialized (e.g. was empty, or did not contain JSON).
        """
        try:
            body_as_json: Dict[str, object] = json.loads(response_body)
        except Exception as exc:
            return None

        try:
            return self._error_response_deserializer.deserialize(body_as_json)
        except DeserializationError as exc:
            return None


    def _get_http_error_response_attribute_value(self, http_error_response: HttpErrorResponse, attribute_key: str) -> str:
        """Gets the value of the specified HttpErrorResponse attribute.
        
        Args:
            http_error_response:
                The HttpErrorResponse to retrieve the attribute from.
            attribute_key:
                The key of the attribute to retrieve.
        Returns:
            The value of the attribute, or a blank string if no attribute with that key exists.
        """

        for current_attribute_value in http_error_response.attributes:
            if (current_attribute_value[0] == attribute_key):
                return current_attribute_value[1]
            
        return ""
    
    #endregion

    #region HTTP Status Exception Throwing Actions

    def _internal_server_error_exception_throwing_action(self, http_error_response: HttpErrorResponse):
        raise RuntimeError(http_error_response.message)


    def _bad_request_exception_throwing_action(self, http_error_response: HttpErrorResponse):
        raise ValueError(http_error_response.message)
    

    def _not_found_exception_throwing_action(self, http_error_response: HttpErrorResponse):
        if (http_error_response.code == "UserNotFoundException"):
            user: str = self._get_http_error_response_attribute_value(http_error_response, "User")
            raise ElementNotFoundError(http_error_response.message, "User", user)
        elif (http_error_response.code == "GroupNotFoundException"):
            group: str = self._get_http_error_response_attribute_value(http_error_response, "Group")
            raise ElementNotFoundError(http_error_response.message, "Group", group)
        elif (http_error_response.code == "EntityTypeNotFoundException"):
            entity_type: str = self._get_http_error_response_attribute_value(http_error_response, "EntityType")
            raise ElementNotFoundError(http_error_response.message, "EntityType", entity_type)
        elif (http_error_response.code == "EntityNotFoundException"):
            entity: str = self._get_http_error_response_attribute_value(http_error_response, "Entity")
            raise ElementNotFoundError(http_error_response.message, "Entity", entity)
        else: 
            resource_id: str = self._get_http_error_response_attribute_value(http_error_response, "ResourceId")
            raise NotFoundError(http_error_response.message, resource_id)

    #endregion
