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
	@coverage run -m unittest discover && coverage report --omit="tests/*"
	@coverage html --omit="tests/*"
	@echo "Coverage Report stored in htmlcov/index.html"