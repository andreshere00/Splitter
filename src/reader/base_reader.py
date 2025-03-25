from abc import ABC, abstractmethod


class BaseReader(ABC):
    @abstractmethod
    def convert(self, file_path: str) -> str | dict:
        pass
