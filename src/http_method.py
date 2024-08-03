from enum import Enum

class HTTPMethod(Enum):
    """Represents an HTTP method.
    """
    GET = "GET", 
    POST = "POST", 
    DELETE = "DELETE"