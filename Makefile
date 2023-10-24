IMAGE_REPO ?= registry.cn-shanghai.aliyuncs.com/kerthcet-public/pr-copilot
GIT_TAG ?= $(shell git describe --tags --dirty --always)
IMAGE_WITH_TAG ?= $(IMAGE_REPO):$(GIT_TAG)

.PHONY: lint
lint:
	mypy .
	black .

.PHONY: test
test: unit-test

.PHONY: unit-test
unit-test: lint
	pytest tests

.PHONY: check
check: lint test

.PHONY: build
build: lint
	echo $(IMAGE_WITH_TAG)
	docker buildx build \
		-f Dockerfile \
		-t $(IMAGE_WITH_TAG) \
		--platform=linux/amd64 \
		--push \
		./ \

.PHONY: export-requirements
export-requirements: export-requirements-dev
	poetry export -f requirements.txt -o requirements.txt --without-hashes

.PHONY: export-requirements-dev
export-requirements-dev:
	poetry export -f requirements.txt -o requirements-dev.txt --without-hashes --with dev

.PHONY: build-zip
build-zip:
	rm -rf ./pr-copilot.zip
	tar --exclude='examples/' \
		--exclude='tests/' \
		--exclude='tmp/' \
		--exclude='.mypy_cache/' \
		--exclude='.pytest_cache/' \
		--exclude='.git/' \
		-zcvf pr-copilot.zip \
		./

.PHONY: run
run:
	serve run main:app model_name_or_path="/workspace/models/meta-llama/llama-2-7b-chat-hf"