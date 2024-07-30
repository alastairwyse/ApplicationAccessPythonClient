from typing import TypeVar, Iterable, Generic, Set, Tuple
from abc import ABC, abstractmethod

TUser = TypeVar("TUser")
TGroup = TypeVar("TGroup")
TComponent = TypeVar("TComponent")
TAccess = TypeVar("TAccess")

class AccessManagerQueryProcessor(Generic[TUser, TGroup, TComponent, TAccess], ABC):
    """Defines methods which query the state/structure of an AccessManager implementation.

    Generic Paramters:
        TUser:
            The type of users in the application.
        TGroup:
            The type of groups in the application.
        TComponent:
            The type of components in the application to manage access to.
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

    @property
    @abstractmethod
    def users(self) -> Iterable[TUser]:
        """Returns a collection of all users in the access manager."""

    @property
    @abstractmethod
    def groups(self) -> Iterable[TGroup]:
        """Returns a collection of all groups in the access manager."""

    @property
    @abstractmethod
    def entity_types(self) -> Iterable[str]:
        """Returns a collection of all entity types in the access manager."""

    def contains_user(self, user: TUser) -> bool:
        """Returns true if the specified user exists.

        Args:
            user: 
                The user check for.    
                
        Returns:
            True if the user exists.  False otherwise.
        """

    def contains_group(self, group: TGroup) -> bool:
        """Returns true if the specified group exists.

        Args:
            user: 
                The group check for.    
                
        Returns:
            True if the group exists.  False otherwise.
        """

    def get_user_to_group_mappings(self, user: TUser, include_indirect_mappings: bool) -> Iterable[TGroup]:
        """Gets the groups that the specified user is mapped to (i.e. is a member of).

        Args:
            user: 
                The user to retrieve the groups for.
            include_indirect_mappings:
                Whether to include indirect mappings (i.e. those that occur via group to group mappings).
                
        Returns:
            A collection of groups the specified user is a member of.
        """

    def get_group_to_user_mappings(self, group: TGroup, includeIndirectMappings: bool) -> Iterable[TUser]:
        """Gets the users that are mapped to the specified group.

        Args:
            group: 
                The group to retrieve the users for.
            include_indirect_mappings:
                Whether to include indirect mappings (i.e. those where a user is mapped to the group via other groups).
                
        Returns:
            A collection of users that are mapped to the specified group.
        """

    def get_group_to_group_mappings(self, group: TGroup, include_indirect_mappings: bool) -> Iterable[TGroup]:
        """Gets the groups that the specified group is mapped to.

        Args:
            group: 
                The group to retrieve the mapped groups for.
            include_indirect_mappings:
                Whether to include indirect mappings (i.e. those where the 'mapped to' group is itself mapped to further groups).
                
        Returns:
            A collection of groups the specified group is mapped to.
        """    

    def get_group_to_group_reverse_mappings(self, group: TGroup, include_indirect_mappings: bool) -> Iterable[TGroup]:
        """Gets the groups that are mapped to the specified group.
        
        Args:
            group: 
                The group to retrieve the mapped groups for.
            include_indirect_mappings:
                Whether to include indirect mappings (i.e. those where the 'mapped from' group is itself mapped from further groups).
                
        Returns:
            A collection of groups that are mapped to the specified group.
        """

    def get_user_to_application_component_and_access_level_mappings(self, user: TUser) -> Iterable[Tuple[TComponent, TAccess]]:
        """Gets the application component and access level pairs that the specified user is mapped to.

        Args:
            user: 
                The user to retrieve the mappings for.
                
        Returns:
            A collection of Tuples containing the application component and access level pairs that the specified user is mapped to.
        """
    def get_application_component_and_access_level_to_user_mappings(self, application_component: TComponent, accesss_level: TAccess, include_indirect_mappings: bool) -> Iterable[TUser]:
        """Gets the users that are mapped to the specified application component and access level pair.

        Args:
            application_component: 
                The application component to retrieve the mappings for.
            accesss_level:
                The access level to retrieve the mappings for.
            include_indirect_mappings:
                Whether to include indirect mappings (i.e. those where a user is mapped to an application component and access level via groups).
        
        Returns:
            A collection of users that are mapped to the specified application component and access level.
        """

    def get_group_to_application_component_and_access_level_mappings(self, group: TGroup) -> Iterable[Tuple[TComponent, TAccess]]:
        """Gets the application component and access level pairs that the specified group is mapped to.

        Args:
            group: 
                The group to retrieve the mappings for.
                
        Returns:
            A collection of Tuples containing the application component and access level pairs that the specified group is mapped to.
        """

    def get_application_component_and_access_level_to_group_mappings(self, application_component: TComponent, accesss_level: TAccess, include_indirect_mappings: bool) -> Iterable[TGroup]:
        """Gets the groups that are mapped to the specified application component and access level pair.

        Args:
            application_component: 
                The application component to retrieve the mappings for.
            accesss_level:
                The access level to retrieve the mappings for.
            include_indirect_mappings:
                Whether to include indirect mappings (i.e. those where a group is mapped to an application component and access level via other groups).

        Returns:
            A collection of groups that are mapped to the specified application component and access level.
        """

    def contains_entity_type(self, entity_type: str) -> bool:
        """Returns true if the specified entity type exists.

        Args:
            entity_type: 
                The entity type to check for.
                
        Returns:
            True if the entity type exists.  False otherwise.
        """

    def get_entities(self, entity_type: str) -> Iterable[str]:
        """Returns all entities of the specified type.

        Args:
            entity_type: 
                The type of the entity.
                
        Returns:
            A collection of all entities of the specified type.
        """

    def contains_entity(self, entity_type: str, entity: str) -> bool:
        """Returns true if the specified entity exists.

        Args:
            entity_type: 
                The type of the entity.
            entity:
                he entity to check for.
                
        Returns:
            True if the entity exists.  False otherwise.
        """

    def get_user_to_entity_mappings_(self, user: TUser) -> Iterable[Tuple[str, str]]:
        """Gets the entities that the specified user is mapped to.

        Args:
            user: 
                The user to retrieve the mappings for.
                
        Returns:
            A collection of Tuples containing the entity type and entity that the specified user is mapped to.
        """ 

    def get_user_to_entity_mappings_for_type(self, user: TUser, entity_type: str) -> Iterable[str]:
        """Gets the entities of a given type that the specified user is mapped to.

        Args:
            user: 
                The user to retrieve the mappings for.
            entity_type:
                The entity type to retrieve the mappings for.
                
        Returns:
            A collection of entities that the specified user is mapped to.
        """ 

    def get_entity_to_user_mappings_(self, entity_type: str, entity: str, include_indirect_mappings: bool) -> Iterable[TUser]:
        """Gets the users that are mapped to the specified entity.
        
        Args:
            entity_type: 
                The entity type to retrieve the mappings for.
            entity:
                The entity to retrieve the mappings for.
            include_indirect_mappings:
                Whether to include indirect mappings (i.e. those where a user is mapped to the entity via groups).
                
        Returns:
            A collection of users that are mapped to the specified entity.
        """

    def get_group_to_entity_mappings_(self, group: TGroup) -> Iterable[Tuple[str, str]]:
        """Gets the entities that the specified group is mapped to.

        Args:
            group: 
                The group to retrieve the mappings for.
                
        Returns:
            A collection of Tuples containing the entity type and entity that the specified group is mapped to.
        """ 

    def get_group_to_entity_mappings_for_type(self, group: TGroup, entity_type: str) -> Iterable[str]:
        """Gets the entities of a given type that the specified group is mapped to.

        Args:
            group: 
                The group to retrieve the mappings for.
            entity_type:
                The entity type to retrieve the mappings for.
                
        Returns:
            A collection of entities that the specified group is mapped to.
        """ 

    def get_entity_to_group_mappings_(self, entity_type: str, entity: str, include_indirect_mappings: bool) -> Iterable[TGroup]:
        """Gets the groups that are mapped to the specified entity.
        
        Args:
            entity_type: 
                The entity type to retrieve the mappings for.
            entity:
                The entity to retrieve the mappings for.
            include_indirect_mappings:
                Whether to include indirect mappings (i.e. those where a group is mapped to the entity via other groups).
                
        Returns:
            A collection of groups that are mapped to the specified entity.
        """

    def has_access_to_application_component(self, user: TUser, application_component: TComponent, access_level: TAccess) -> bool:
        """Checks whether the specified user (or a group that the user is a member of) has access to an application component at the specified level of access.

        Args:
            user: 
                The user to check for.
            application_component:
                The application component.
            access_level:
                The level of access to the component.
        Returns:
            True if the user has access the component.  False otherwise.
        """

    def has_access_to_entity(self, user: TUser, entity_type: str, entity: str) -> bool:
        """Checks whether the specified user (or a group that the user is a member of) has access to the specified entity.

        Args:
            user: 
                The user to check for.
            entity_type:
                The type of the entity.
            entity:
                The entity.
        Returns:
            True if the user has access the entity.  False otherwise.
        """

    def get_application_components_accesible_by_user(self, user: TUser) -> Set[Tuple[TComponent, TAccess]]:
        """Gets all application components and levels of access that the specified user (or a group that the user is a member of) has access to.

        Args:
            user: 
                The user to retrieve the application components and levels of access for.
                
        Returns:
            The application components and levels of access to those application components that the user has access to.
        """

    def get_application_components_accesible_by_group(self, group: TGroup) -> Set[Tuple[TComponent, TAccess]]:
        """Gets all application components and levels of access that the specified group (or a group that the specified group is a member of) has access to.

        Args:
            group: 
                The group to retrieve the application components and levels of access for.
                
        Returns:
            The application components and levels of access to those application components that the group has access to.
        """

    def get_entities_accessible_by_user(self, user: TUser) -> Set[Tuple[str, str]]:
        """Gets all entities that the specified user (or a group that the user is a member of) has access to.

        Args:
            user: 
                The user to retrieve the entities for.
                
        Returns:
            A collection of Tuples containing the entity type and entity that the user has access to.
        """

    def get_entities_accessible_by_user(self, user: TUser, entity_type: str) -> Set[str]:
        """Gets all entities of a given type that the specified user (or a group that the user is a member of) has access to.

        Args:
            user: 
                The user to retrieve the entities for.
            entity_type:
                The type of entities to retrieve.
                
        Returns:
            The entities the user has access to.
        """

    def get_entities_accessible_by_group(self, group: TGroup) -> Set[Tuple[str, str]]:
        """Gets all entities that the specified group (or a group that the specified group is a member of) has access to.

        Args:
            group: 
                The group to retrieve the entities for.
                
        Returns:
            A collection of Tuples containing the entity type and entity that the group has access to.
        """

    def get_entities_accessible_by_group(self, group: TGroup, entity_type: str) -> Set[str]:
        """Gets all entities of a given type that the specified group (or a group that the specified group is a member of) has access to.

        Args:
            group: 
                The group to retrieve the entities for.
            entity_type:
                The type of entities to retrieve.
                
        Returns:
            The entities the group has access to.
        """
