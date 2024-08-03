from typing import TypeVar, Iterable, Generic
from abc import ABC, abstractmethod

TUser = TypeVar("TUser")
TGroup = TypeVar("TGroup")
TComponent = TypeVar("TComponent")
TAccess = TypeVar("TAccess")

class AccessManagerEventProcessor(Generic[TUser, TGroup, TComponent, TAccess], ABC):
    """Defines methods to process events which change the structure of an AccessManager implementation.

    Generic Paramters:
        TUser:
            The type of users in the application.
        TGroup:
            The type of groups in the application.
        TComponent:
            The type of components in the application to manage access to.
        TAccess:
            The type of levels of access which can be assigned to an application component.
    """

    def add_user(self, user: TUser) -> None:
        """Adds a user.

        Args:
            user: 
                The user to add.       
        """

    def remove_user(self, user: TUser) -> None:
        """Removes a user.

        Args:
            user: 
                The user to remove.       
        """

    def add_group(self, group: TGroup) -> None:
        """Adds a group.

        Args:
            group: 
                The group to add.       
        """

    def remove_group(self, group: TGroup) -> None:
        """Removes a group.

        Args:
            group: 
                The group to remove.       
        """

    def add_user_to_group_mapping(self, user: TUser, group: TGroup) -> None:
        """Adds a mapping between the specified user and group.

        Args:
            user: 
                The user in the mapping.
            group: 
                The group in the mapping.
        """

    def remove_user_to_group_mapping(self, user: TUser, group: TGroup) -> None:
        """Removes the mapping between the specified user and group.

        Args:
            user: 
                The user in the mapping.
            group: 
                The group in the mapping.
        """

    def add_group_to_group_mapping(self, from_group: TGroup, to_group: TGroup) -> None:
        """Adds a mapping between the specified groups.

        Args:
            from_group: 
                The 'from' group in the mapping.
            to_group: 
                The 'to' group in the mapping.
        """

    def remove_group_to_group_mapping(self, from_group: TGroup, to_group: TGroup) -> None:
        """Removes the mapping between the specified groups.
        
        Args:
            from_group: 
                The 'from' group in the mapping.
            to_group: 
                The 'to' group in the mapping.
        """

    def add_user_to_application_component_and_access_level_mapping(self, user: TUser, application_component: TComponent, access_level: TAccess) -> None:
        """Adds a mapping between the specified user, application component, and level of access to that component.
        
        Args:
            user: 
                The user in the mapping.
            application_component:
                The application component in the mapping.
            access_level:
                The level of access to the component.
        """ 

    def remove_user_to_application_component_and_access_level_mapping(self, user: TUser, application_component: TComponent, access_level: TAccess) -> None:
        """Removes a mapping between the specified user, application component, and level of access to that component.
        
        Args:
            user: 
                The user in the mapping.
            application_component:
                The application component in the mapping.
            access_level:
                The level of access to the component.
        """ 

    def add_group_to_application_component_and_access_level_mapping(self, group: TGroup, application_component: TComponent, access_level: TAccess) -> None:
        """Adds a mapping between the specified group, application component, and level of access to that component.
        
        Args:
            group: 
                The group in the mapping.
            application_component:
                The application component in the mapping.
            access_level:
                The level of access to the component.
        """ 

    def remove_group_to_application_component_and_access_level_mapping(self, group: TGroup, application_component: TComponent, access_level: TAccess) -> None:
        """Removes a mapping between the specified group, application component, and level of access to that component.
        
        Args:
            group: 
                The group in the mapping.
            application_component:
                The application component in the mapping.
            access_level:
                The level of access to the component.
        """ 

    def add_entity_type(self, entity_type: str) -> None:
        """Adds an entity type.
        
        Args:
            entity_type: 
                The entity type to add.
        """  

    def remove_entity_type(self, entity_type: str) -> None:
        """Removes an entity type.
        
        Args:
            entity_type: 
                The entity type to remove.
        """  

    def add_entity(self, entity_type: str, entity: str) -> None:
        """Adds an entity.
        
        Args:
            entity_type: 
                The type of the entity.
            entity:
                The entity to add.
        """

    def remove_entity(self, entity_type: str, entity: str) -> None:
        """Removes an entity.
        
        Args:
            entity_type: 
                The type of the entity.
            entity:
                The entity to remove.
        """

    def add_user_to_entity_mapping(self, user: TUser, entity_type: str, entity: str) -> None:
        """Adds a mapping between the specified user, and entity.
        
        Args:
            user: 
                The user in the mapping.
            entity_type:
                The type of the entity.
            entity:
                The entity in the mapping.
        """

    def remove_user_to_entity_mapping(self, user: TUser, entity_type: str, entity: str) -> None:
        """Removes a mapping between the specified user, and entity.
        
        Args:
            user: 
                The user in the mapping.
            entity_type:
                The type of the entity.
            entity:
                The entity in the mapping.
        """

    def add_group_to_entity_mapping(self, group: TGroup, entity_type: str, entity: str) -> None:
        """Adds a mapping between the specified group, and entity.
        
        Args:
            group: 
                The group in the mapping.
            entity_type:
                The type of the entity.
            entity:
                The entity in the mapping.
        """

    def remove_group_to_entity_mapping(self, group: TGroup, entity_type: str, entity: str) -> None:
        """Removes a mapping between the specified group, and entity.
        
        Args:
            group: 
                The group in the mapping.
            entity_type:
                The type of the entity.
            entity:
                The entity in the mapping.
        """
