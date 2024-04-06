PYTHON_VERSION = 3.11.7
VIRTUAL_ENV = gmail-integration

init:
	@conda create --name $(VIRTUAL_ENV) python=$(PYTHON_VERSION) --yes
	@echo "Conda environment $(VIRTUAL_ENV) created with Python $(PYTHON_VERSION)"
	@echo "Run 'conda activate $(VIRTUAL_ENV)' to activate the environment"

install:
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt
	@pip install -r requirements-test.txt

test:
	@coverage run -m unittest discover && coverage report --omit="tests/*"
	@coverage html --omit="tests/*"

run_fetch_emails:
	@python src/fetch_emails.py

run_email_rule_processor:
	@python src/email_rule_processor.py
