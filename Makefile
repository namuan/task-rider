export PROJECTNAME=$(shell basename "$(PWD)")

.SILENT: ;               # no need for @

install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@uv run pre-commit install

clean: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -delete
	@rm -rf build/ dist/

black: ## Runs black for code formatting
	uv run -- black app --exclude generated

lint: black ## Runs Flake8 for linting
	uv run -- flake8 app

setup: clean ## Re-initiates virtualenv
	rm -rf .venv
	uv sync --group dev

deps: ## Reinstalls dependencies
	uv sync --group dev

uic: res ## Converts ui files in resources/views to python
	for i in `ls resources/views/*.ui`; do FNAME=`basename $${i} ".ui"`; uv run -- pyuic6 $${i} > "app/generated/$${FNAME}_ui.py"; done

res: ## Generates and compresses resource listed in resources/resources.qrc
	echo "Not supported in PyQt6"

package: clean ## Run installer
	@uv run pyinstaller main.spec --clean

install-macosx: package ## Installs application in users Application folder
	./scripts/install-macosx.sh TaskRider.app

ICON_PNG ?= assets/$(PROJECTNAME)-icon.png

icons: ## Generate ICNS and ICO files from the PNG logo
	@bash assets/generate-icons.sh $(ICON_PNG)

run: ## Runs the application
	uv run task-rider

context: clean ## Build context file from application sources
	echo "Generating context"
	llm-context-builder.py --extensions .py --ignored_dirs build dist generated venv .venv .idea --print_contents --temp_file

.PHONY: help
.DEFAULT_GOAL := setup

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo
