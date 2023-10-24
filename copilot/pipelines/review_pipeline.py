from llmlite.apis import ChatLLM, ChatMessage  # type: ignore

from copilot.pipelines.pipeline import Pipeline
from copilot.pipelines.templates.review_template import (
    REVIEW_SYSTEM_PROMPT,
    REVIEW_USER_PROMPT,
)
from copilot.providers.github_provider import get_pr_info
from copilot.utils.log import rayserve_logger


class ReviewPipeline(Pipeline):
    """
    ReviewPipeline is used for review the PR.
    """

    def __init__(self, llm: ChatLLM) -> None:
        super().__init__(llm)
        self.logger = rayserve_logger()

    def completion(self, url: str) -> str | None:
        pr_info = get_pr_info(url=url)

        # TODO:
        user_prompt = REVIEW_USER_PROMPT.format(
            title=pr_info["title"],
            description=pr_info["description"],
            commit_messages=pr_info["commit_messages"],
            pr_diffs=pr_info["pr_diffs"],
        )

        self.logger.debug("user prompt: {prompt}".format(prompt=user_prompt))

        return self.llm.completion(
            messages=[
                ChatMessage(role="system", content=REVIEW_SYSTEM_PROMPT),
                ChatMessage(role="user", content=user_prompt),
            ],
        )
