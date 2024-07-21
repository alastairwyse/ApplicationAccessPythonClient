class DeserializationError(Exception):
    """The error that is thrown when deserialization fails.
    """
        
    def __init__(self, message: str) -> None:
        """Initialises a new instance of the DeserializationError class.
        
        Args:
            message:   
                The message that describes the error.
        """
        super().__init__(message)

    __doc__ += Exception.__doc__
