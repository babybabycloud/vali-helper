.PHONY: test_dep
test_dep:
	pip install pytest pytest-cov

.PHONY: test
test: test_dep
	pytest

.PHONY: cover
cover: test_dep
	pytest --cov=vali --cov-report=html vali/tests/
