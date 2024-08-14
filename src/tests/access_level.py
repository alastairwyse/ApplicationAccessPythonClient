from enum import Enum

class AccessLevel(Enum):
    """Represents different levels of access to components within an application.
    """
    view = 0, 
    create = 1, 
    modify = 2, 
    delete = 3, 
    reserved_characters = 4