.PHONY: batch drought flood wildfire tests

.SHELLFLAGS = -ec

# Useful for building images locally for debugging purposes
drought:
	docker build -t apinine-drought \
	--target production --build-arg GEOTIFF_PATH=$$GEOTIFF_PATH -f drought/baseline/Dockerfile .

flood:
	docker build -t apinine-flood \
	--target production --build-arg GEOTIFF_PATH=$$GEOTIFF_PATH -f flood/baseline/Dockerfile .

flood_rcp:
	docker build -t apinine-flood-rcp \
	--target production --build-arg GEOTIFF_PATH=$$GEOTIFF_PATH -f flood/rcp/Dockerfile .


wildfire:
	docker build -t apinine-wildfire \
	--target production --build-arg GEOTIFF_PATH=$$GEOTIFF_PATH -f wildfire/baseline/Dockerfile .

schema_test:
	cd common; pip install -r requirements-dev.txt; pytest

.ONESHELL:
tests:
	pip install -e common/geocoder
	pip install -e common/readgeodata
	pip install -e common/land_use
	pip install -r common/requirements-dev.txt; pytest common/tests
	pip install -r drought/requirements-dev.txt; pytest drought
	pip install -r flood/requirements-dev.txt; pytest flood
	pip install -r wildfire/requirements-dev.txt; pytest wildfire
	pip install -r user/requirements-dev.txt; pytest user
	pip install -r map/requirements-dev.txt; pytest map
	pip install -r batch_request/requirements-dev.txt; pytest batch_request

.ONESHELL:
tests_unit:
	pip install -e common/geocoder
	pip install -e common/readgeodata
	pip install -e common/land_use
	pip install -r common/requirements-dev.txt; pytest common/tests -m unit
	pip install -r drought/requirements-dev.txt; pytest drought -m unit
	pip install -r flood/requirements-dev.txt; pytest flood -m unit
	pip install -r wildfire/requirements-dev.txt; pytest wildfire -m unit
	pip install -r user/requirements-dev.txt; pytest user -m unit
	pip install -r map/requirements-dev.txt; pytest map -m unit
	pip install -r batch_request/requirements-dev.txt; pytest batch_request -m unit

docker_risks:
	docker build --target test -f flood/baseline/Dockerfile .
	docker build --target test -f flood/rcp/Dockerfile .
	docker build --target test -f drought/baseline/Dockerfile .
	docker build --target test -f wildfire/baseline/Dockerfile .
	docker build --target test -f user/Dockerfile .
	docker build --target test -f map/flood/baseline/Dockerfile --build-arg GITHUB_TOKEN=$$GITHUB_TOKEN .
	docker build --target test -f batch_request/flood/baseline/Dockerfile .

.ONESHELL:
test_cognito:
	pip install -r get_token/requirements-dev.txt; pytest get_token


.ONESHELL:
test_cognito_unit:
	pip install -r get_token/requirements-dev.txt; pytest get_token -m unit

docker_cognito:
	cd get_token; docker build --target test .
