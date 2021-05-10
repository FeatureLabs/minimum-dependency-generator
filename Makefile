.PHONY: clean
clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '*~' -delete

.PHONY: lint
lint:
	flake8 minimum_dependency_generator/
	isort --check-only minimum_dependency_generator/

.PHONY: lint-fix
lint-fix:
	autopep8 --in-place --recursive --max-line-length=100 minimum_dependency_generator/
	isort minimum_dependency_generator/

.PHONY: test
test: lint
	pytest minimum_dependency_generator/ --cache-clear --show-capture=stderr

.PHONY: testcoverage
testcoverage: lint
	pytest minimum_dependency_generator/ --cov=minimum_dependency_generator  --cov-config=.coveragerc --cache-clear --show-capture=stderr
