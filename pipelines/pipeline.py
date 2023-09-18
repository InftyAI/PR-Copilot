from abc import ABC, abstractmethod


class Pipeline(ABC):
    @abstractmethod
    def completion(self, url: str, return_format: str) -> str:
        """
        Args:
            url (str): The PR link.
            return_format: The result format of function chat(), it can be `json`, `yaml`, etc..
        """
        pass
