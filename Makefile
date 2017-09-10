default: help

develop: ## setup develop mode
	python setup.py develop
.PHONY: develop

init: ## install the requirements
	python setup.py install
.PHONY: init

test: ## run the tests
	flake8 --exclude=.git,build --ignore=E501 .
	py.test --cov=enasearch tests/
.PHONY: test

upload: ## upload on PyPi
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
.PHONY: upload

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help