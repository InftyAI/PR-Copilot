from typing import Dict, Literal

from ray import serve
from llmlite.apis import ChatLLM  # type: ignore
from ray.serve import Application
from fastapi import FastAPI
from pydantic import BaseModel
import torch

# from copilot.pipelines.review_pipeline import ReviewPipeline
from copilot.pipelines.summary_pipeline import SummaryPipeline
from copilot.utils.envs import GITHUB_TOKEN
from copilot.utils.log import rayserve_logger

app = FastAPI()

DEFAULT_MODEL = "codellama/CodeLlama-7b-hf"
DEFAULT_TASK = "text-generation"


# Item helps to constrain the request parameters.
class Item(BaseModel):
    url: str


@serve.deployment(
    route_prefix="/agent",
    ray_actor_options={
        "num_cpus": 1,
        "num_gpus": 1,
    },
    autoscaling_config={"min_replicas": 1, "max_replicas": 1},
)
@serve.ingress(app)
class AgentDeployment:
    def __init__(
        self,
        model_name_or_path: str,
        task: str,
        torch_dtype: torch.dtype = torch.float16,
    ) -> None:
        """
        Args:
            model_name_or_path (str): The model name or the model path.
            task (str): The task defining which pipeline will be returned.
            torch_dtype (torch.dtype): The precision for this model.
        """
        llm = ChatLLM(
            model_name_or_path=model_name_or_path, task=task, torch_dtype=torch_dtype
        )
        self.summary_pipeline = SummaryPipeline(llm)
        # self.review_pipeline = ReviewPipeline(llm)

        self.logger = rayserve_logger()

    # TODO
    @app.get("/pr-review/")
    def review(self, item: Item):
        """
        Args:
            item (Item): The POST body should include the url.
        """

        self.logger.debug("request parameters: {item}".format(item=item))
        # return self.review_pipeline.completion(url=item.url)

    @app.post("/pr-summary/")
    def summary(self, item: Item):
        """
        Args:
            item (Item): The POST body should include the url.
        """

        self.logger.debug("request parameters: {item}".format(item=item))
        return self.summary_pipeline.completion(url=item.url)


def app_builder(args: Dict[Literal["model_name_or_path", "task"], str]) -> Application:
    """
    Args:
        model_name_or_path: default to "codellama/CodeLlama-7b-hf"
        task: default to "text-generation"
    """

    model = (
        args["model_name_or_path"]
        if "model_name_or_path" in args.keys()
        else DEFAULT_MODEL
    )
    task = args["task"] if "task" in args.keys() else DEFAULT_TASK

    if GITHUB_TOKEN is None or GITHUB_TOKEN == "":
        raise ("noe github token provided")

    return AgentDeployment.bind(  # type: ignore
        model_name_or_path=model,
        task=task,
    )
