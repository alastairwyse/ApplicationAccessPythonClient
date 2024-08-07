from typing import Dict, Set, List, TypeVar, Iterable, Generic, Tuple

from src.json_array_to_iterable_converter import JsonArrayToIterableConverter
from unique_stringifier_base import UniqueStringifierBase
from string_unique_stringifier import StringUniqueStringifier
from access_manager_client_base import AccessManagerClientBase
from access_manager_event_processor import AccessManagerEventProcessor
from access_manager_query_processor import AccessManagerQueryProcessor

TUser = TypeVar("TUser")
TGroup = TypeVar("TGroup")
TComponent = TypeVar("TComponent")
TAccess = TypeVar("TAccess")

class AccessManagerClient(AccessManagerClientBase, AccessManagerEventProcessor, AccessManagerQueryProcessor, Generic[TUser, TGroup, TComponent, TAccess]):
    """Client class which interfaces to an AccessManager instance hosted as a REST web API.

    Generic Paramters:
        TUser:
            The type of users in the AccessManager.
        TGroup:
            The type of groups in the AccessManager.
        TComponent:
            The type of components in the AccessManager.
        TAccess:
            The type of levels of access which can be assigned to an application component.

    Attributes:
        users:
            Returns a collection of all users in the access manager.
        groups:
            Returns a collection of all groups in the access manager.
        entity_types:
            Returns a collection of all entity types in the access manager.
    
    """

    _USER_JSON_NAME: str = "user"
    _GROUP_JSON_NAME: str = "group"
    _FROM_GROUP_JSON_NAME: str = "fromGroup"
    _TO_GROUP_JSON_NAME: str = "toGroup"
    _APPLICATION_COMPONENT_JSON_NAME: str = "applicationComponent"
    _ACCESS_LEVEL_JSON_NAME: str = "accessLevel"
    _ENTITY_TYPE_JSON_NAME: str = "entityType"
    _ENTITY_JSON_NAME: str = "entity"

    def __init__(
            self,
            base_url: str, 
            user_stringifier: UniqueStringifierBase[TUser], 
            group_stringifier: UniqueStringifierBase[TGroup], 
            application_component_stringifier: UniqueStringifierBase[TComponent], 
            access_level_stringifier: UniqueStringifierBase[TAccess], 
            headers: Dict[str, str]=dict(), 
            auth=None, 
            timeout=65536, 
            proxies=None, 
            verify=None, 
            cert=None
        ) -> None:
        """Initialises a new instance of the AccessManagerClient class.

        Optionsl parameters ('auth', 'timeout', 'proxies', etc...) when set, are passed directly to the underlying requests.request() methods.  
        See the requests documentation (https://requests.readthedocs.io/) for documentation, type definitions, and usage examples of these parameters.
        
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
            headers:
                An optional Dict containing HTTP header neam/value pairs to send with each request to the AccessManager instance.
        """
        super().__init__(
            base_url, 
            user_stringifier, 
            group_stringifier, 
            application_component_stringifier, 
            access_level_stringifier, 
            headers=headers, 
            auth=auth, 
            timeout=timeout, 
            proxies=proxies, 
            verify=verify, 
            cert=cert
        )
        self._json_to_iterable_converter: JsonArrayToIterableConverter = JsonArrayToIterableConverter()


    @property
    def users(self) -> Iterable[TUser]:
        url: str = self._base_url + "users"
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TUser] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._user_stringifier)
        
        return results


    @property
    def groups(self) -> Iterable[TGroup]:
        url: str = self._base_url + "groups"
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TGroup] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._group_stringifier)
        
        return results


    @property
    def entity_types(self) -> Iterable[str]:
        url: str = self._base_url + "entityTypes"
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        
        return raw_results


    def add_user(self, user: TUser) -> None:
        url: str = self._base_url + "users/{0}".format(
            self._user_stringifier.to_string(user)
            )

        self._send_post_request(url)


    def contains_user(self, user: TUser) -> bool:
        url: str = self._base_url + "users/{0}".format(
            self._encode_url_component(self._user_stringifier.to_string(user))
            )
        
        return self._send_get_request_for_contains_method(url)


    def remove_user(self, user: TUser) -> None:
        url: str = self._base_url + "users/{0}".format(
            self._encode_url_component(self._user_stringifier.to_string(user))
            )

        self._send_delete_request(url)
    

    def add_group(self, group: TGroup) -> None:
        url: str = self._base_url + "groups/{0}".format(
            self._encode_url_component(self._group_stringifier.to_string(group))
            )

        self._send_post_request(url)
    

    def contains_group(self, group: TGroup) -> bool:
        url: str = self._base_url + "groups/{0}".format(
            self._encode_url_component(self._group_stringifier.to_string(group))
            )

        return self._send_get_request_for_contains_method(url)
    

    def remove_group(self, group: TGroup) -> None:
        url: str = self._base_url + "groups/{0}".format(
            self._encode_url_component(self._group_stringifier.to_string(group))
            )

        self._send_delete_request(url)
    

    def add_user_to_group_mapping(self, user: TUser, group: TGroup) -> None:
        url: str = self._base_url + "userToGroupMappings/user/{0}/group/{1}".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(self._group_stringifier.to_string(group))
        )

        self._send_post_request(url)
    

    def get_user_to_group_mappings(self, user: TUser, include_indirect_mappings: bool) -> Iterable[TGroup]:
        url: str = self._base_url + "userToGroupMappings/user/{0}?includeIndirectMappings={1}".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            str.lower(str(include_indirect_mappings))
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TGroup] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._group_stringifier, self._GROUP_JSON_NAME)
        
        return results
    

    def get_group_to_user_mappings(self, group: TGroup, include_indirect_mappings: bool) -> Iterable[TUser]:
        url: str = self._base_url + "userToGroupMappings/group/{0}?includeIndirectMappings={1}".format(
            self._encode_url_component(self._group_stringifier.to_string(group)), 
            str.lower(str(include_indirect_mappings))
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TUser] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._user_stringifier, self._USER_JSON_NAME)
        
        return results
    

    def remove_user_to_group_mapping(self, user: TUser, group: TGroup) -> None:
        url: str = self._base_url + "userToGroupMappings/user/{0}/group/{1}".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(self._group_stringifier.to_string(group))
        )

        self._send_delete_request(url)
    

    def add_group_to_group_mapping(self, from_group: TGroup, to_group: TGroup) -> None:
        url: str = self._base_url + "groupToGroupMappings/fromGroup/{0}/toGroup/{1}".format(
            self._encode_url_component(self._group_stringifier.to_string(from_group)), 
            self._encode_url_component(self._group_stringifier.to_string(to_group))
        )

        self._send_post_request(url)
    

    def get_group_to_group_mappings(self, group: TGroup, include_indirect_mappings: bool) -> Iterable[TGroup]:
        url: str = self._base_url + "groupToGroupMappings/group/{0}?includeIndirectMappings={1}".format(
            self._encode_url_component(self._group_stringifier.to_string(group)), 
            str.lower(str(include_indirect_mappings))
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TGroup] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._group_stringifier, self._TO_GROUP_JSON_NAME)
        
        return results
    

    def get_group_to_group_reverse_mappings(self, group: TGroup, include_indirect_mappings: bool) -> Iterable[TGroup]:
        url: str = self._base_url + "groupToGroupReverseMappings/group/{0}?includeIndirectMappings={1}".format(
            self._encode_url_component(self._group_stringifier.to_string(group)), 
            str.lower(str(include_indirect_mappings))
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TGroup] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._group_stringifier, self._FROM_GROUP_JSON_NAME)
        
        return results
    

    def remove_group_to_group_mapping(self, from_group: TGroup, to_group: TGroup) -> None:
        url: str = self._base_url + "groupToGroupMappings/fromGroup/{0}/toGroup/{1}".format(
            self._encode_url_component(self._group_stringifier.to_string(from_group)), 
            self._encode_url_component(self._group_stringifier.to_string(to_group))
        )

        self._send_delete_request(url)
    

    def add_user_to_application_component_and_access_level_mapping(self, user: TUser, application_component: TComponent, access_level: TAccess) -> None:
        url: str = self._base_url + "userToApplicationComponentAndAccessLevelMappings/user/{0}/applicationComponent/{1}/accessLevel/{2}".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(self._application_component_stringifier.to_string(application_component)), 
            self._encode_url_component(self._access_level_stringifier.to_string(access_level))
        )

        self._send_post_request(url)
    

    def get_user_to_application_component_and_access_level_mappings(self, user: TUser) -> Iterable[Tuple[TComponent, TAccess]]:
        url: str = self._base_url + "userToApplicationComponentAndAccessLevelMappings/user/{0}?includeIndirectMappings=false".format(
            self._encode_url_component(self._user_stringifier.to_string(user))
        )
        raw_results = self._send_get_request(url)
        results: Iterable[Tuple[TComponent, TAccess]] = self._json_to_iterable_converter.convert_to_iterable_of_tuples(
            raw_results, # type: ignore
            self._APPLICATION_COMPONENT_JSON_NAME, 
            self._ACCESS_LEVEL_JSON_NAME, 
            self._application_component_stringifier, 
            self._access_level_stringifier
            )
        
        return results
    

    def get_application_component_and_access_level_to_user_mappings(self, application_component: TComponent, accesss_level: TAccess, include_indirect_mappings: bool) -> Iterable[TUser]:
        url: str = self._base_url + "userToApplicationComponentAndAccessLevelMappings/applicationComponent/{0}/accessLevel/{1}?includeIndirectMappings={2}".format(
            self._encode_url_component(self._application_component_stringifier.to_string(application_component)), 
            self._encode_url_component(self._access_level_stringifier.to_string(accesss_level)), 
            str.lower(str(include_indirect_mappings))
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TUser] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._user_stringifier, self._USER_JSON_NAME)
        
        return results
    
    
    def remove_user_to_application_component_and_access_level_mapping(self, user: TUser, application_component: TComponent, access_level: TAccess) -> None:
        url: str = self._base_url + "userToApplicationComponentAndAccessLevelMappings/user/{0}/applicationComponent/{1}/accessLevel/{2}".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(self._application_component_stringifier.to_string(application_component)), 
            self._encode_url_component(self._access_level_stringifier.to_string(access_level))
        )

        self._send_delete_request(url)


    def add_group_to_application_component_and_access_level_mapping(self, group: TGroup, application_component: TComponent, access_level: TAccess) -> None:
        url: str = self._base_url + "groupToApplicationComponentAndAccessLevelMappings/group/{0}/applicationComponent/{1}/accessLevel/{2}".format(
            self._encode_url_component(self._group_stringifier.to_string(group)), 
            self._encode_url_component(self._application_component_stringifier.to_string(application_component)), 
            self._encode_url_component(self._access_level_stringifier.to_string(access_level))
        )

        self._send_post_request(url)
    

    def get_group_to_application_component_and_access_level_mappings(self, group: TGroup) -> Iterable[Tuple[TComponent, TAccess]]:
        url: str = self._base_url + "groupToApplicationComponentAndAccessLevelMappings/group/{0}?includeIndirectMappings=false".format(
            self._encode_url_component(self._group_stringifier.to_string(group))
        )
        raw_results = self._send_get_request(url)
        results: Iterable[Tuple[TComponent, TAccess]] = self._json_to_iterable_converter.convert_to_iterable_of_tuples(
            raw_results, # type: ignore
            self._APPLICATION_COMPONENT_JSON_NAME, 
            self._ACCESS_LEVEL_JSON_NAME, 
            self._application_component_stringifier, 
            self._access_level_stringifier
            )
        
        return results
    

    def get_application_component_and_access_level_to_group_mappings(self, application_component: TComponent, accesss_level: TAccess, include_indirect_mappings: bool) -> Iterable[TGroup]:
        url: str = self._base_url + "groupToApplicationComponentAndAccessLevelMappings/applicationComponent/{0}/accessLevel/{1}?includeIndirectMappings={2}".format(
            self._encode_url_component(self._application_component_stringifier.to_string(application_component)), 
            self._encode_url_component(self._access_level_stringifier.to_string(accesss_level)), 
            str.lower(str(include_indirect_mappings))
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TGroup] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._group_stringifier, self._GROUP_JSON_NAME)
        
        return results
    

    def remove_group_to_application_component_and_access_level_mapping(self, group: TGroup, application_component: TComponent, access_level: TAccess) -> None:
        url: str = self._base_url + "groupToApplicationComponentAndAccessLevelMappings/group/{0}/applicationComponent/{1}/accessLevel/{2}".format(
            self._encode_url_component(self._group_stringifier.to_string(group)), 
            self._encode_url_component(self._application_component_stringifier.to_string(application_component)), 
            self._encode_url_component(self._access_level_stringifier.to_string(access_level))
        )

        self._send_delete_request(url)
    

    def add_entity_type(self, entity_type: str) -> None:
        url: str = self._base_url + "entityTypes/{0}".format(
            self._encode_url_component(entity_type)
            )

        self._send_post_request(url)
    

    def contains_entity_type(self, entity_type: str) -> bool:
        url: str = self._base_url + "entityTypes/{0}".format(
            self._encode_url_component(entity_type)
            )

        return self._send_get_request_for_contains_method(url)


    def remove_entity_type(self, entity_type: str) -> None:
        url: str = self._base_url + "entityTypes/{0}".format(
            self._encode_url_component(entity_type)
            )

        self._send_delete_request(url)


    def add_entity(self, entity_type: str, entity: str) -> None:
        url: str = self._base_url + "entityTypes/{0}/entities/{1}".format(
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity)
        )

        self._send_post_request(url)


    def get_entities(self, entity_type: str) -> Iterable[str]:  
        url: str = self._base_url + "entityTypes/{0}/entities".format(
            self._encode_url_component(entity_type)
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[str] = self._json_to_iterable_converter.convert_to_iterable(raw_results, StringUniqueStringifier(), self._ENTITY_JSON_NAME)
        
        return results


    def contains_entity(self, entity_type: str, entity: str) -> bool:
        url: str = self._base_url + "entityTypes/{0}/entities/{1}".format(
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity)
        )

        return self._send_get_request_for_contains_method(url)

    
    def remove_entity(self, entity_type: str, entity: str) -> None:
        url: str = self._base_url + "entityTypes/{0}/entities/{1}".format(
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity)
        )

        self._send_delete_request(url)

    
    def add_user_to_entity_mapping(self, user: TUser, entity_type: str, entity: str) -> None:
        url: str = self._base_url + "userToEntityMappings/user/{0}/entityType/{1}/entity/{2}".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity)
        )

        self._send_post_request(url)


    def get_user_to_entity_mappings(self, user: TUser) -> Iterable[Tuple[str, str]]:
        url: str = self._base_url + "userToEntityMappings/user/{0}?includeIndirectMappings=false".format(
            self._encode_url_component(self._user_stringifier.to_string(user))
        )
        raw_results = self._send_get_request(url)
        results: Iterable[Tuple[str, str]] = self._json_to_iterable_converter.convert_to_iterable_of_tuples(
            raw_results, # type: ignore
            self._ENTITY_TYPE_JSON_NAME, 
            self._ENTITY_JSON_NAME, 
            StringUniqueStringifier(), 
            StringUniqueStringifier()
            )
        
        return results


    def get_user_to_entity_mappings_for_type(self, user: TUser, entity_type: str) -> Iterable[str]:
        url: str = self._base_url + "userToEntityMappings/user/{0}/entityType/{1}?includeIndirectMappings=false".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(entity_type)
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[str] = self._json_to_iterable_converter.convert_to_iterable(raw_results, StringUniqueStringifier(), self._ENTITY_JSON_NAME)
        
        return results


    def get_entity_to_user_mappings(self, entity_type: str, entity: str, include_indirect_mappings: bool) -> Iterable[TUser]:
        url: str = self._base_url + "userToEntityMappings/entityType/{0}/entity/{1}?includeIndirectMappings={2}".format(
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity), 
            str.lower(str(include_indirect_mappings))
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TUser] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._user_stringifier, self._USER_JSON_NAME)
        
        return results


    def remove_user_to_entity_mapping(self, user: TUser, entity_type: str, entity: str) -> None:
        url: str = self._base_url + "userToEntityMappings/user/{0}/entityType/{1}/entity/{2}".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity)
        )

        self._send_delete_request(url)


    def add_group_to_entity_mapping(self, group: TGroup, entity_type: str, entity: str) -> None:
        url: str = self._base_url + "groupToEntityMappings/group/{0}/entityType/{1}/entity/{2}".format(
            self._encode_url_component(self._group_stringifier.to_string(group)), 
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity)
        )

        self._send_post_request(url)


    def get_group_to_entity_mappings(self, group: TGroup) -> Iterable[Tuple[str, str]]:
        url: str = self._base_url + "groupToEntityMappings/group/{0}?includeIndirectMappings=false".format(
            self._encode_url_component(self._group_stringifier.to_string(group))
        )
        raw_results = self._send_get_request(url)
        results: Iterable[Tuple[str, str]] = self._json_to_iterable_converter.convert_to_iterable_of_tuples(
            raw_results, # type: ignore
            self._ENTITY_TYPE_JSON_NAME, 
            self._ENTITY_JSON_NAME, 
            StringUniqueStringifier(), 
            StringUniqueStringifier()
            )
        
        return results


    def get_group_to_entity_mappings_for_type(self, group: TGroup, entity_type: str) -> Iterable[str]:
        url: str = self._base_url + "groupToEntityMappings/group/{0}/entityType/{1}?includeIndirectMappings=false".format(
            self._encode_url_component(self._group_stringifier.to_string(group)), 
            self._encode_url_component(entity_type)
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[str] = self._json_to_iterable_converter.convert_to_iterable(raw_results, StringUniqueStringifier(), self._ENTITY_JSON_NAME)
        
        return results


    def get_entity_to_group_mappings(self, entity_type: str, entity: str, include_indirect_mappings: bool) -> Iterable[TGroup]:
        url: str = self._base_url + "groupToEntityMappings/entityType/{0}/entity/{1}?includeIndirectMappings={2}".format(
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity), 
            str.lower(str(include_indirect_mappings))
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[TGroup] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._group_stringifier, self._GROUP_JSON_NAME)
        
        return results


    def remove_group_to_entity_mapping(self, group: TGroup, entity_type: str, entity: str) -> None:
        url: str = self._base_url + "groupToEntityMappings/group/{0}/entityType/{1}/entity/{2}".format(
            self._encode_url_component(self._group_stringifier.to_string(group)), 
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity)
        )

        self._send_delete_request(url)

    
    def has_access_to_application_component(self, user: TUser, application_component: TComponent, access_level: TAccess) -> bool:
        url: str = self._base_url + "dataElementAccess/applicationComponent/user/{0}/applicationComponent/{1}/accessLevel/{2}".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(self._application_component_stringifier.to_string(application_component)), 
            self._encode_url_component(self._access_level_stringifier.to_string(access_level)), 
        )
        results = self._send_get_request(url)
        assert isinstance(results, bool)

        return results


    def has_access_to_entity(self, user: TUser, entity_type: str, entity: str) -> bool:
        url: str = self._base_url + "dataElementAccess/entity/user/{0}/entityType/{1}/entity/{2}".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(entity_type), 
            self._encode_url_component(entity), 
        )
        results = self._send_get_request(url)
        assert isinstance(results, bool)

        return results


    def get_application_components_accesible_by_user(self, user: TUser) -> Set[Tuple[TComponent, TAccess]]:
        url: str = self._base_url + "userToApplicationComponentAndAccessLevelMappings/user/{0}?includeIndirectMappings=true".format(
            self._encode_url_component(self._user_stringifier.to_string(user))
        )
        raw_results = self._send_get_request(url)
        results: Iterable[Tuple[TComponent, TAccess]] = self._json_to_iterable_converter.convert_to_iterable_of_tuples(
            raw_results, # type: ignore
            self._APPLICATION_COMPONENT_JSON_NAME, 
            self._ACCESS_LEVEL_JSON_NAME, 
            self._application_component_stringifier, 
            self._access_level_stringifier
            )
        
        return set(results)


    def get_application_components_accesible_by_group(self, group: TGroup) -> Set[Tuple[TComponent, TAccess]]:
        url: str = self._base_url + "groupToApplicationComponentAndAccessLevelMappings/group/{0}?includeIndirectMappings=true".format(
            self._encode_url_component(self._group_stringifier.to_string(group))
        )
        raw_results = self._send_get_request(url)
        results: Iterable[Tuple[TComponent, TAccess]] = self._json_to_iterable_converter.convert_to_iterable_of_tuples(
            raw_results, # type: ignore
            self._APPLICATION_COMPONENT_JSON_NAME, 
            self._ACCESS_LEVEL_JSON_NAME, 
            self._application_component_stringifier, 
            self._access_level_stringifier
            )
        
        return set(results)


    def get_entities_accessible_by_user(self, user: TUser) -> Set[Tuple[str, str]]:
        url: str = self._base_url + "userToEntityMappings/user/{0}?includeIndirectMappings=true".format(
            self._encode_url_component(self._user_stringifier.to_string(user))
        )
        raw_results = self._send_get_request(url)
        results: Iterable[Tuple[str, str]] = self._json_to_iterable_converter.convert_to_iterable_of_tuples(
            raw_results, # type: ignore
            self._ENTITY_TYPE_JSON_NAME, 
            self._ENTITY_JSON_NAME, 
            StringUniqueStringifier(), 
            StringUniqueStringifier()
            )
        
        return set(results)


    def get_entities_of_type_accessible_by_user(self, user: TUser, entity_type: str) -> Set[str]:
        url: str = self._base_url + "userToEntityMappings/user/{0}/entityType/{1}?includeIndirectMappings=true".format(
            self._encode_url_component(self._user_stringifier.to_string(user)), 
            self._encode_url_component(entity_type)
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[str] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._group_stringifier, self._ENTITY_JSON_NAME)
        
        return set(results)


    def get_entities_accessible_by_group(self, group: TGroup) -> Set[Tuple[str, str]]:
        url: str = self._base_url + "groupToEntityMappings/group/{0}?includeIndirectMappings=true".format(
            self._encode_url_component(self._group_stringifier.to_string(group))
        )
        raw_results = self._send_get_request(url)
        results: Iterable[Tuple[str, str]] = self._json_to_iterable_converter.convert_to_iterable_of_tuples(
            raw_results, # type: ignore
            self._ENTITY_TYPE_JSON_NAME, 
            self._ENTITY_JSON_NAME, 
            StringUniqueStringifier(), 
            StringUniqueStringifier()
            )
        
        return set(results)


    def get_entities_of_type_accessible_by_group(self, group: TGroup, entity_type: str) -> Set[str]:
        url: str = self._base_url + "groupToEntityMappings/group/{0}/entityType/{1}?includeIndirectMappings=true".format(
            self._encode_url_component(self._group_stringifier.to_string(group)), 
            self._encode_url_component(entity_type)
        )
        raw_results = self._send_get_request(url)
        assert isinstance(raw_results, List)
        results: Iterable[str] = self._json_to_iterable_converter.convert_to_iterable(raw_results, self._group_stringifier, self._ENTITY_JSON_NAME)
        
        return set(results)



    __doc__ += AccessManagerEventProcessor.__doc__ # type: ignore
    __doc__ += AccessManagerQueryProcessor.__doc__ # type: ignore

