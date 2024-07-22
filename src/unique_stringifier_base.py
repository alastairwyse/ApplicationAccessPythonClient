from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")

class UniqueStringifierBase(Generic[T], ABC):
    """Base class for converting objects of a specified type to and from strings which uniquely identify the object.

    Generic Paramters:
        T:
            The type of objects to convert.
    """

    @abstractmethod
    def to_string(self, input_object: T) -> str:
        """Converts an object into a string which uniquely identifies that object.
        
        Args:
            input_object:
                The object to convert.
        
        Returns:
            A string which uniquely identifies that object.
        """

    @abstractmethod
    def from_string(self, stringified_object: str) -> T:
        """Converts a string which uniquely identifies an object into the object.
        
        Args:
            stringified_object:
                The string representing the object.
        
        Returns:
            The object.
        """
