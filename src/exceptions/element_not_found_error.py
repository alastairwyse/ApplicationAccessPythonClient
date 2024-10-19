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

from src.exceptions.not_found_error import NotFoundError

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

    __doc__ += NotFoundError.__doc__ # type: ignore
