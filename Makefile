.PHONY: init

PYTHON_VERSION = 3.11.7
VIRTUAL_ENV = gmail-integration

init:
	@conda create --name $(VIRTUAL_ENV) python=$(PYTHON_VERSION) --yes
	@conda activate $(VIRTUAL_ENV)

install:
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt
	@pip install -r requirements-test.txt

test:
	PYTHONPATH=$(shell pwd)/src:$(shell pwd)/tests/ coverage run -m discover $(PYTHONPATH) && coverage report --omit="tests/*,venv/*"
	@coverage html --omit="tests/*,venv/*"
	@echo "Coverage Report stored in htmlcov/index.html"