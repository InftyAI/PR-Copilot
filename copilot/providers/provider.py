from abc import ABC, abstractmethod
from typing import Dict


class Provider(ABC):
    def __init__(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def get_pr_info(self, url: str) -> Dict[str, str]:
        """
        Args:
            url: The pr link.

        Return:
            A dict contains keys as below:
                title (str):
                description (str):
                commit_messages (array[string]):
                git_diffs (str):
        """
        pass
