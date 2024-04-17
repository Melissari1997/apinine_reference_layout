.PHONY: drought flood wildfire tests

.SHELLFLAGS = -ec

# Useful for building images locally for debugging purposes
drought:
	docker build -t apinine-drought \
	--target production --build-arg GEOTIFF_PATH=$$GEOTIFF_PATH -f drought/Dockerfile .

flood:
	docker build -t apinine-flood \
	--target production --build-arg GEOTIFF_PATH=$$GEOTIFF_PATH -f flood/Dockerfile .

wildfire:
	docker build -t apinine-wildfire \
	--target production --build-arg GEOTIFF_PATH=$$GEOTIFF_PATH -f wildfire/Dockerfile .

schema_test:
	cd common; pip install -r requirements-dev.txt; pytest

.ONESHELL:
tests:
	pip install -e common/geocoder
	pip install -e common/readgeodata
	pip install -r drought/requirements-dev.txt; pytest drought
	pip install -r flood/requirements-dev.txt; pytest flood
	pip install -r wildfire/requirements-dev.txt; pytest wildfire
	pip install -r user/requirements-dev.txt; pytest user

.ONESHELL:
tests_unit:
	pip install -e common/geocoder
	pip install -e common/readgeodata
	pip install -r drought/requirements-dev.txt; pytest drought -m unit
	pip install -r flood/requirements-dev.txt; pytest flood -m unit
	pip install -r wildfire/requirements-dev.txt; pytest wildfire -m unit
	pip install -r user/requirements-dev.txt; pytest user -m unit

docker_risks:
	docker build --target test -f flood/Dockerfile .
	docker build --target test -f drought/Dockerfile .
	docker build --target test -f wildfire/Dockerfile .
	docker build --target test -f user/Dockerfile .

.ONESHELL:
test_cognito:
	pip install -r get_token/requirements-dev.txt; pytest get_token


.ONESHELL:
test_cognito_unit:
	pip install -r get_token/requirements-dev.txt; pytest get_token -m unit

docker_cognito:
	cd get_token; docker build --target test .
