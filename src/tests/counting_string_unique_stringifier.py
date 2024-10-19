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

from src.string_unique_stringifier import StringUniqueStringifier

class CountingStringUniqueStringifier(StringUniqueStringifier):
    """Subclass of StringUniqueStringifier used for testing which counts the number of calls to the to_string() and from_string() methods."""

    @property
    def to_string_count(self) -> int:
        """The number of times the to_string() method has been called."""
        return self._to_string_count

    @property
    def from_string_count(self) -> int:
        """The number of times the from_string() method has been called."""
        return self._from_string_count

    def __init__(self) -> None:
        """Initialises a new instance of the CountingStringUniqueStringifier class."""
        super().__init__()
        self._to_string_count: int = 0
        self._from_string_count: int = 0

    def to_string(self, input_object: str) -> str:

        self._to_string_count += 1
        return super().to_string(input_object)

    def from_string(self, stringified_object: str) -> str:

        self._from_string_count += 1
        return super().from_string(stringified_object)