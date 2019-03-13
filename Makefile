install-dev:
	pip3 install -r requirements-dev.txt
.PHONY: install-dev

install:
	pip3 install -r requirements.txt
.PHONY: install

test-lambda:
	python-lambda-local -f handler -t 300 iosreviews.py event.json
.PHONY: test-lambda

