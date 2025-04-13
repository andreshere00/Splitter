from abc import ABC, abstractmethod
from typing import List


class BaseReader(ABC):
    """
    Abstract class which implements Readers.
    """

    @abstractmethod
    def convert(self, file_path: str) -> str | dict | List[str]:
        pass
