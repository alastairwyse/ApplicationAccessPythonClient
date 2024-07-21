from not_found_error import NotFoundError

class ElementNotFoundError(NotFoundError):
    """The exception that is thrown when a element was not found in an AccessManager instance.

    Attributes:
        element_type:
            The type of the element.
        element_value:
            The value of the element.
    """

    @property
    def element_type(self) -> str:
        """The type of the element."""
        return self._element_type
    
    @property
    def element_value(self) -> str:
        """The value of the element."""
        return self.resource_id
    
    def __init__(self, message: str, element_type: str, element_value: str) -> None:
        """Initialises a new instance of the ElementNotFoundError class.
        
        Args:
            message:   
                The message that describes the error.
            element_type:
                The type of the element.
            element_value:
                The value of the element.
        """
        super().__init__(message, element_value)
        self._element_type: str = element_type

    __doc__ += NotFoundError.__doc__
