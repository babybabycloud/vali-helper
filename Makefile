SHELL := /bin/bash
ifeq ($(COV_REPORT_TYPE),)
COV_REPORT_TYPE := term
endif

.PHONY: upgrade_pip
upgrade_pip:
	pip install pip --upgrade

.PHONY: build_dep
build_dep: upgrade_pip
	pip install build

.PHONY: build
build: build_dep
	python -m build

.PHONY: install
install: build
	pip install dist/*.whl

.PHONY: check
check: install test cover lint type

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
lint: lint_dep
	pylint vali

.PHONY: mypy_dep
mypy_dep: upgrade_pip
	pip install mypy

.PHONY: type
type: mypy_dep
	mypy vali/

.PHONY: tox_dep
tox_dep: upgrade_pip
	pip install tox

.PHONY: tox
tox: tox_dep
	tox --colored yes

.PHONY: develop
develop: upgrade_pip
	pip install -e . --config-settings editable_mode=strict
	
.PHONY: upload_dep
upload_dep：upgrade_pip
	pip install twine

.PHONY: upload
upload: build upload_dep
	python -m twine upload --username __token__ --password ${PYPI_PASSWORD} dist/*

.PHONY: clean
clean:
        pip uninstall -y vali-helper && \
        rm -rf build dist
