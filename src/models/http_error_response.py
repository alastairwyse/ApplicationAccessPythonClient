from typing import Iterable, Tuple

class HttpErrorResponse:
    """Container class holding the data returned from a REST API when an error occurs.

    Attributes:
        code:
            An internal code representing the error.
        message:
            A description of the error.
        target:
            The target of the error.
        attributes:
            A collection of key/value pairs which give additional details of the error.
        inner_error:
            The error which caused this error.
    """

    @property
    def code(self) -> str:
        """An internal code representing the error."""
        return self._code

    @property
    def message(self) -> str:
        """A description of the error."""
        return self._message

    @property
    def target(self) -> str:
        """The target of the error."""
        return self._target

    @property
    def attributes(self) -> Iterable[Tuple[str, str]]:
        """A collection of key/value pairs which give additional details of the error."""
        return self._attributes

    @property
    def inner_error(self) -> "HttpErrorResponse":
        """The error which caused this error."""
        return self._inner_error

    def __init__(
            self, 
            code: str, 
            message: str, 
            target: str=None, 
            attributes: Iterable[Tuple[str, str]]=[], 
            inner_error:"HttpErrorResponse"=None
            ) -> None:
        """Initialises a new instance of the HttpErrorResponse class.

        Args:
            code:   
                An internal code representing the error.
            message:
                A description of the error.
            target:
                The target of the error.
            attributes:
                A collection of key/value pairs which give additional details of the error.
            inner_error:
                The error which caused this error.
        """

        # Ordinarily would have exception handlers here for null or whitespace 'code' and 'message' parameters...
        #   However since instances of this class will likely be created as part of exception handling code, we don't want to throw further exceptions and risk hiding/losing the original exception details.
        
        self._code: str = code
        self._message: str = message
        self._target: str = target
        self._attributes: Iterable[Tuple[str, str]] = attributes
        self._inner_error: "HttpErrorResponse" = inner_error





    