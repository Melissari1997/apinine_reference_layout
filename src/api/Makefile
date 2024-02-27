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
	cd common; pytest

.ONESHELL:
tests:
	pytest drought
	pytest flood
	pytest wildfire
