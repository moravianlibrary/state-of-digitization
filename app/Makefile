PYTHON_VERSION := python3.12
PYTHON_VENV_DIR := .venv
PYTHON := $(PYTHON_VENV_DIR)/bin/python
PIP := $(PYTHON_VENV_DIR)/bin/pip
PYTHON_REQUIREMENTS := requirements.txt

SERVER_RUNNER := uvicorn
APP_ENTRYPOINT := app:app

.PHONY: generate-env remove-env regenerate-env

generate-env:
	$(PYTHON_VERSION) -m venv $(PYTHON_VENV_DIR)
	$(PYTHON) -m ensurepip
	$(PIP) install --upgrade pip
	$(PIP) install -r $(PYTHON_REQUIREMENTS)

remove-env:
	rm -rf $(PYTHON_VENV_DIR)

regenerate-env: remove-env generate-env

run:
	$(PYTHON) -m $(SERVER_RUNNER) $(APP_ENTRYPOINT)
