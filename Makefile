.PHONY: run
run:
	serve run main:app

unit-test: unit-test
	pytest tests
