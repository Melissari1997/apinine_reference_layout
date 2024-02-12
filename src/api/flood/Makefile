.PHONY: flood tests

.SHELLFLAGS = -ec

.ONESHELL:
flood:
	cd ..
	docker build -t apinine-flood --target production -f flood/Dockerfile .
	cd flood

tests:
	pytest
