class NotFoundError(ValueError):
    """The exception that is thrown when a resource doesn't exist or could not be found.

    Attributes:
        resource_id:
            A unique identifier for the resource.
    """

    @property
    def resource_id(self) -> str:
        """A unique identifier for the resource."""
        return self._resource_id
    
    def __init__(self, message: str, resource_id: str) -> None:
        """Initialises a new instance of the NotFoundError class.
        
        Args:
            message:   
                The message that describes the error.
            resource_id:
                A unique identifier for the resource.
        """
        super().__init__(message)
        self._eleme_resource_idnt_value: str = resource_id

    __doc__ += ValueError.__doc__