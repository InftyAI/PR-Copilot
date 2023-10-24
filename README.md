# PR-Copilot

Your AI pair programmer 🤖️ specialized in code review, code summary and even code completion. 🧑‍💻🐛

## How to use

Still under developing, once we've done, you can @agent for requests.

## How to install

Step 1. Run `poetry install` to initialize the environment.

Step 2. Run `export GITHUB_TOKEN=<your github token>` to set the token which is required when requesting the github API.

Step 3. Run `serve run main:app model_name_or_path=<your model name> task=<your task name>` to serve your application. The model is default to `codellama/CodeLlama-7b-hf`, task is default to `text-generation`.

## Roadmap

- Ignore useless files, like auto-generated
- Support Gitlab
- Text split when the diff is quite big
