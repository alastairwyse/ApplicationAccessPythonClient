# Clients might need to offer ability to pass CA file (possible in Python)... python allows client side certificate too
# Python does allow automatic retries
# Java looks like it allows passing a HTTPClient
# Allow passing custom headers??
# Allow user to set timeout
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 

from typing import TypeVar, Iterable, Generic, Set, Tuple

from access_manager_event_processor import AccessManagerEventProcessor
from access_manager_query_processor import AccessManagerQueryProcessor

TUser = TypeVar("TUser")
TGroup = TypeVar("TGroup")
TComponent = TypeVar("TComponent")
TAccess = TypeVar("TAccess")

class AccessManagerClient(Generic[TUser, TGroup, TComponent, TAccess], AccessManagerEventProcessor, AccessManagerQueryProcessor):
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


    __doc__ += AccessManagerEventProcessor.__doc__
    __doc__ += AccessManagerQueryProcessor.__doc__