from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union


class BaseConverter(ABC):
    """
    Abstract base class for file converters.

    Define the interface for converting an input file into an output file
    of a specified format. Subclasses must override the `convert` method
    to implement the actual conversion logic.
    """

    @abstractmethod
    def convert(
        self, input_source: Union[str, Path], output_target: Union[str, Path]
    ) -> None:
        """
        Convert the input file to the specified output file.

        Read the content from `input_source`, perform the conversion to the
        target format, and write the result to `output_target`.

        Parameters:
            input_source (str or Path): Path to the source file.
            output_target (str or Path): Path where the converted file will be saved.

        Raises:
            ConversionError: If the conversion process fails.
        """
        ...


# Example of a custom exception you might use:
class ConversionError(Exception):
    """Raised when a conversion cannot be completed."""

    pass
