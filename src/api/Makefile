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
	pytest drought
	pytest flood
	pytest wildfire

.ONESHELL:
tests_unit:
	pip install -e common/geocoder
	pip install -e common/readgeodata
	pip install -r drought/requirements-dev.txt; pytest drought -m unit
	pip install -r flood/requirements-dev.txt; pytest flood -m unit
	pip install -r wildfire/requirements-dev.txt; pytest wildfire -m unit
