.PHONY: wildfire tests

.SHELLFLAGS = -ec

.ONESHELL:
wildfire:
	cd ..
	docker build -t testsrcctx -f wildfire/Dockerfile .
	docker run testsrcctx

tests:
	pytest
