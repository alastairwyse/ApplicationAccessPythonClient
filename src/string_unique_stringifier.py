from unique_stringifier_base import UniqueStringifierBase

class StringUniqueStringifier(UniqueStringifierBase[str]):
    """An implementation of UniqueStringifierBase[T] for strings."""

    def to_string(self, input_object: str) -> str:

        return input_object

    def from_string(self, stringified_object: str) -> str:

        return stringified_object