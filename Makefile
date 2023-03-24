.PHONY: test_dep
test_dep:
	pip install coverage pytest

.PHONY: test
test: test_dep
	pytest

.PHONY: cover
cover: test_dep
	coverage run -m pytest && coverage html
