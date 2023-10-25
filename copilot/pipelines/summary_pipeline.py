from llmlite.apis import ChatLLM, ChatMessage  # type: ignore

from copilot.pipelines.pipeline import Pipeline
from copilot.pipelines.templates.summary_template import (
    SUMMARY_SYSTEM_PROMPT,
    SUMMARY_USER_PROMPT,
)
from copilot.providers.github_provider import GitHubProvider
from copilot.utils.log import rayserve_logger


class SummaryPipeline(Pipeline):
    """
    SummaryPipeline is used for summary the PR.
    """

    def __init__(self, llm: ChatLLM) -> None:
        super().__init__(llm)
        self.logger = rayserve_logger()

    def completion(self, url: str) -> str | None:
        pr_info = GitHubProvider.get_pr_info(url=url)
        user_prompt = SUMMARY_USER_PROMPT.format(
            title=pr_info["title"],
            description=pr_info["description"],
            commit_messages=pr_info["commit_messages"],
            pr_diffs=pr_info["pr_diffs"],
        )

        self.logger.debug("user prompt: {prompt}".format(prompt=user_prompt))

        return self.llm.completion(
            messages=[
                ChatMessage(role="system", content=SUMMARY_SYSTEM_PROMPT),
                ChatMessage(role="user", content=user_prompt),
            ],
            promptMode="instruct",
            max_length=8192,
            return_full_text=False,
        )
