1.DEFAULT_GOAL := lint

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: lint
lint:
	flake8
