init:
	python setup.py install

test:
	flake8 --exclude=.git,build .
	python setup.py test

upload:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi

.PHONY: init test