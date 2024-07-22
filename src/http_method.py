from enum import Enum

class HTTPMethod(Enum):
    """Represents an HTTP method.
    """
    get = "GET", 
    post = "POST", 
    delete = "DELETE"