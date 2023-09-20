.PHONY: run
run:
	serve run main:app model_name_or_path="/data/models/meta-llama/llama-2-7b-chat-hf"

unit-test: unit-test
	pytest tests
