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

from typing import Dict

from src.access_manager_client import AccessManagerClient
from src.string_unique_stringifier import StringUniqueStringifier

class AccessManagerStringElementClient(AccessManagerClient):
    """Client class which interfaces to an AccessManager instance hosted as a REST web API, where users, groups, application components, and access levels are strings.

    Attributes:
        users:
            Returns a collection of all users in the access manager.
        groups:
            Returns a collection of all groups in the access manager.
        entity_types:
            Returns a collection of all entity types in the access manager.
    
    """

    def __init__(
            self,
            base_url: str, 
            headers: Dict[str, str]=dict(), 
            auth=None, 
            timeout=65536, 
            proxies=None, 
            verify=None, 
            cert=None
        ) -> None:
        """Initialises a new instance of the AccessManagerStringElementClient class.

        Optionsl parameters ('auth', 'timeout', 'proxies', etc...) when set, are passed directly to the underlying requests.request() methods.  
        See the requests documentation (https://requests.readthedocs.io/) for documentation, type definitions, and usage examples of these parameters.
        
        Args:
            base_url:
                The base URL for the hosted Web API (must include a trailing forward slash).
            headers:
                An optional Dict containing HTTP header neam/value pairs to send with each request to the AccessManager instance.
        """
        super().__init__(
            base_url, 
            StringUniqueStringifier(), 
            StringUniqueStringifier(), 
            StringUniqueStringifier(), 
            StringUniqueStringifier(), 
            headers=headers, 
            auth=auth, 
            timeout=timeout, 
            proxies=proxies, 
            verify=verify, 
            cert=cert
        )


    __doc__ += AccessManagerClient.__doc__ # type: ignore