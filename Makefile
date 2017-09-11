# Sphinx variable
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = enasearch
SOURCEDIR     = src/docs
BUILDDIR      = tmp


# Commands
default: help

init: ## install the requirements
	python setup.py install
	pip install Sphinx
.PHONY: init

develop: init ## setup develop mode
	python setup.py develop
.PHONY: develop

test: ## run the tests
	flake8 --exclude=.git,build --ignore=E501 .
	py.test --cov=enasearch tests/
.PHONY: test

upload: ## upload on PyPi
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
.PHONY: upload

doc: ## generate HTML documentation
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	rm -rf docs
	mv "$(BUILDDIR)/html" docs
.PHONY: doc

data: ## generate the data
	python bin/serialize_ena_data_descriptors.py
.PHONY: data

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help