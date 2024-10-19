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
        self._resource_id: str = resource_id

    __doc__ += ValueError.__doc__ # type: ignore