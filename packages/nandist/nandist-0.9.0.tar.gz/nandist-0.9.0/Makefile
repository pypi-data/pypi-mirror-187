.dummy: test build devenv external clean_manual

.ONESHELL:

.SHELLFLAGS := -euo pipefail -c
SHELL := bash

venv:
	python3.10 -m venv venv
	source venv/bin/activate
	pip install -r requirements-dev.txt

devenv: venv
	source venv/bin/activate
	mypy --install-types

manual: venv clean_manual
	source venv/bin/activate
	sphinx-build docs pages

clean_manual:
	rm -rf pages

build:
	rm dist/*
	flit build

publish_test: build
	twine upload --repository testpypi dist/*

publish: build
	twine upload --repository pypi dist/*


test: build
	tox -p
