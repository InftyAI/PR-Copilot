from abc import ABC, abstractmethod

from llmlite.apis import ChatLLM  # type: ignore


class Pipeline(ABC):
    def __init__(self, llm: ChatLLM) -> None:
        self.llm = llm

    @abstractmethod
    def completion(self, content: str) -> str | None:
        """
        Args:
            url (str): The PR link.
        """
        pass
