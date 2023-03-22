.PHONY: test
test:
	python -m unittest discover -s vali/tests

.PHONY: cover
cover:
	coverage run -m unittest discover -s vali/tests && coverage html
