SHELL := /bin/bash
ifeq ($(COV_REPORT_TYPE),)
COV_REPORT_TYPE := term
endif

.PHONY: check
check: test cover lint type

.PHONY: upgrade_pip
upgrade_pip:
	pip install pip --upgrade

.PHONY: test_dep
test_dep: upgrade_pip
	pip install pytest pytest-cov

.PHONY: test
test: test_dep
	pytest

.PHONY: cover
cover: test_dep
	pytest --cov=vali --cov-report=$(COV_REPORT_TYPE) vali/tests/

.PHONY: lint_dep
lint_dep: upgrade_pip
	pip install pylint

.PHONY: lint
lint:
	pylint vali

.PHONY: mypy_dep
mypy_dep:
	pip install mypy

.PHONY: type
type: mypy_dep
	mypy vali/

.PHONY: tox_dep
tox_dep:
	pip install tox

.PHONY: tox
tox: tox_dep
	tox --colored yes

.PHONY:
develop:
	pip install -e . --config-settings editable_mode=strict

.PHONY: distribute_dep
distribute_dep: upgrade_pip
	pip install build twine

.PHONY: upload
upload: distribute_dep
	python -m build && \
	python -m twine upload --repository testpypi --username __token__ --password ${PYPI_PASSWORD} dist/*
