from typing import List

from llmlite.apis import ChatLLM, ChatMessage  # type: ignore

from copilot.utils.log import rayserve_logger


class GenPipeline:
    """
    GenPipeline is used for generate the code.
    """

    def __init__(self, llm: ChatLLM) -> None:
        # super().__init__(llm)
        self.llm = llm
        self.logger = rayserve_logger()

    def completion(
        self,
        messages: List[ChatMessage],
    ) -> str | None:
        """
        Args:
            content (str): The user prompt.
        """
        # self.logger.debug("user prompt: {prompt}".format(prompt=content))

        return self.llm.completion(
            messages=messages,
            promptMode="instruct",
            max_length=8192,
            return_full_text=False,
        )
