from abc import ABC, abstractmethod


class BaseReader(ABC):
    """
    Abstract class which implements Readers.
    """

    @abstractmethod
    def convert(self, file_path: str) -> str | dict:
        pass
