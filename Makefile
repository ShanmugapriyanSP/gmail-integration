
PYTHON_VERSION = 3.11.7

init:
	pyenv install $(PYTHON_VERSION) --skip-existing
	pyenv local $(PYTHON_VERSION)
	python -m venv venv
#	ifeq ($(OS),Windows_NT)
#    	$activate = .venv/Scripts/activate
#	else
#    	$activate = .venv/bin/activate
#	endif

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-test.txt

test:
	PYTHONPATH=$(shell pwd)/src:$(shell pwd)/tests/ coverage run -m discover $(PYTHONPATH) && coverage report --omit="tests/*,venv/*"
	coverage html --omit="tests/*,venv/*"
	echo "Coverage Report stored in htmlcov/index.html"