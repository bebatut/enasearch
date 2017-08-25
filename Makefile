develop:
	python setup.py develop

init:
	python setup.py install

test:
	flake8 --exclude=.git,build --ignore=E501 .
	pytest --cov=enasearch tests/

upload:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi

.PHONY: init test