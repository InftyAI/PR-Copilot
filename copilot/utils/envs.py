import os

LOG_LEVEL = os.getenv("LOG_LEVEL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:4000"
