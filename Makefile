init:
	python setup.py install

test:
	flake8 --exclude=.git,build .
	python setup.py test

.PHONY: init test