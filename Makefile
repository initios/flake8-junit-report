ENVPATH		        ?= .venv
REQUIREMENTS        ?= requirements.txt
TEST_REQUIREMENTS   ?= requirements_dev.txt

all: help

help: ## Show available targets message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

## Configure virtual environment and install dependencies
venv-configure: ## Configure virtual environment and install dependencies
	@echo ">>> Configure virtual environment..."
	python -m venv $(ENVPATH)
	. $(ENVPATH)/bin/activate
	@echo ">>> Activated virtual environment..."

venv-activate: ## Activate virtual-env
	. $(ENVPATH)/bin/activate
	@echo ">>> Activated virtual environment..."

install-dependencies: ## Install dependencies from requirements
	pip install -r $(REQUIREMENTS)

install-dev-dependencies: ## Install dev dependencies
	pip install -r $(TEST_REQUIREMENTS)

test-unit: ## Run unit tests
	coverage run -m pytest --junitxml="unit-test-result.xml"
	coverage xml

black: ## Apply auto lint changes using black
	black --check . -l 127 --exclude .venv/

lint: ## Run linter analysis
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --statistics

.PHONY: help venv-configure venv-activate install-dependencies install-dev-dependencies test-unit black lint
