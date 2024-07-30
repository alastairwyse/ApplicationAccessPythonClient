from string_unique_stringifier import StringUniqueStringifier

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