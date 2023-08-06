.PHONY: install-dev flake8 lint format test shell docsgen


install-dev:
	pip install '.[dev]'
	pip install '.[doc]'

flake8:
	flake8 ons

lint:
	./scripts/lint.sh

format:
	./scripts/format.sh

test:
	./scripts/test-integration.sh

shell:
	ipython

docsgen:
	pdoc3 -f --skip-errors --html -o docs ons