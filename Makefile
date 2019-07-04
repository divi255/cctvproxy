VERSION=0.0.2

all:
	@echo "what do you want to build today?"

ver:
	find . -type f -name "*.py" -exec sed -i "s/^__version__ = .*/__version__ = \'${VERSION}\'/g" {} \;

d:
	rm -rf dist
	python3 setup.py sdist

pub-test:
	twine upload -r test dist/*

pub-pypi:
	twine upload dist/*

