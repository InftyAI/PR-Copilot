from typing import Dict, Literal

from ray import serve
from ray.serve import Application
from fastapi import FastAPI
from pydantic import BaseModel
import torch

from pipelines.summary_pipeline import SummaryPipeline
from utils.log import rayserve_logger

app = FastAPI()


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
class CopilotDeployment:
    def __init__(
        self,
        model_name_or_path: str = None,
        task: str = None,
        torch_dtype: torch.dtype = torch.float16,
    ) -> None:
        """
        Args:
            model_name_or_path (str): The model name or the model path.
            task (str): The task defining which pipeline will be returned.
            torch_dtype (torch.dtype): The precision for this model.
        """
        self.summary_pipeline = SummaryPipeline(
            model_name_or_path=model_name_or_path, task=task, torch_dtype=torch_dtype
        )
        self.logger = rayserve_logger()

    # TODO
    @app.get("/pr-review")
    def review(self):
        pass

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
        else "codellama/CodeLlama-7b-hf"
    )
    task = args["task"] if "task" in args.keys() else "text-generation"

    return CopilotDeployment.bind(
        model_name_or_path=model,
        task=task,
    )
