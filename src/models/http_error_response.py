#
# Copyright 2024 Alastair Wyse (https://github.com/alastairwyse/ApplicationAccessPythonClient/)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Iterable, Tuple, Union

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
    def target(self) -> Union[str, None]:
        """The target of the error."""
        return self._target

    @property
    def attributes(self) -> Iterable[Tuple[str, str]]:
        """A collection of key/value pairs which give additional details of the error."""
        return self._attributes

    @property
    def inner_error(self) -> Union["HttpErrorResponse", None]:
        """The error which caused this error."""
        return self._inner_error

    def __init__(
            self, 
            code: str, 
            message: str, 
            target: Union[str, None]=None, 
            attributes: Iterable[Tuple[str, str]]=[], 
            inner_error: Union["HttpErrorResponse", None]=None
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
        self._target: Union[str, None] = target
        self._attributes: Iterable[Tuple[str, str]] = attributes
        self._inner_error: Union["HttpErrorResponse", None] = inner_error





    