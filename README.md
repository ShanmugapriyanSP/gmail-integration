# gmail-integration

This repository contains Python scripts for fetching emails and processing email rules. Below are the instructions 
for setting up the virtual environment and running the provided scripts using a Makefile or from a terminal.

## Project Structure
* `conf`:  Holds files like `config.yml`, `credentials.json`, and `rules.json`.
* `src`: Stores Python scripts.
* `tests`: Includes Python unit & mocked e2e tests.
* `Makefile`: Provides commands for convenient setup and script execution.
* `requirements.txt`: Lists project dependencies.
* `requirements-test.txt`: Lists test dependencies.

## Pre-requisites
Make sure you have `miniconda`, `make` and `PostgreSQL` installed on your system. 

## Setup

To create a Python virtual environment using miniconda, run:
```commandline
make init
```
The `install` command installs the both project and test dependencies
```commandline
make install
```
The `test` command executes mocked tests and generates a coverage report:
```commandline
make test
```

### IDE Configuration
To avoid import errors, mark the `src` directory as `Sources Root` and `tests` directory as `Test Sources Root`.  
If you are using Pycharm, right click on the directory and then choose `Mark Directory As`.

## Running Scripts
* Follow the steps mentioned in [Setting up OAuth 2.0](https://support.google.com/googleapi/answer/6158849?hl=en) 
page to generate the client secret and store the json file as `credentials.json` under `conf` directory.
* Modify the script configurable parameters as per your need which is located in `conf/config.yml`.
* Ensure PostgreSQL database is running.

### Fetch Emails
To run the fetch emails script, execute the following command.
```commandline
python src/fetch_emails.py
```
OR
```commandline
make run_fetch_emails
```

### Email Rule Processor
To run the email rule processor script, execute the following command.
```commandline
python src/email_rule_processor.py
```
OR
```commandline
make run_email_rule_processor
```



## Reference

[Gmail API Python Documentation](https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/index.html)