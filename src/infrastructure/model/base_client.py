from abc import ABC, abstractmethod
from typing import Optional


class BaseLLMClient(ABC):
    """
    Abstract base class for LLM clients.
    """

    @abstractmethod
    def get_client(self) -> object:
        """
        Returns the underlying LLM client instance.
        """
        pass

    @abstractmethod
    def get_model(self) -> Optional[str]:
        """
        Returns the model name if applicable.
        """
        pass

    def is_enabled(self) -> bool:
        """
        Returns True if the client is active.
        """
        return self.get_client() is not None
