from enum import Enum

class HTTPMethod(Enum):
    """Represents an HTTP method.
    """
    get = "GET", 
    put = "PUT", 
    delete = "DELETE"