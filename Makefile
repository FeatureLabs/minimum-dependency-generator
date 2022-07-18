.PHONY: clean
clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '*~' -delete

.PHONY: lint
lint:
	isort --check-only minimum_dependency_generator/
	black minimum_dependency_generator -t py310 --check

.PHONY: lint-fix
lint-fix:
	black minimum_dependency_generator -t py310
	isort minimum_dependency_generator/

.PHONY: test
test:
	pytest minimum_dependency_generator/ --cache-clear --show-capture=stderr

.PHONY: testcoverage
testcoverage:
	pytest minimum_dependency_generator/ --cov=minimum_dependency_generator  --cov-config=.coveragerc --cache-clear --show-capture=stderr

.PHONY: installdeps
installdeps:
	pip install -r requirements.txt
	pip install -r test-requirements.txt
