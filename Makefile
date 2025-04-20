init:
	python -m pip install -r requirements-dev.txt

test:
	tox -p

format:
	black --config ./pyproject.toml ./src
	isort ./src

coverage:
	python -m pytest --verbose --cov-report term --cov-report xml --cov=src/brrt tests

build: 
	python setup.py sdist bdist_wheel