format:
	@ruff check

fix-format:
	@ruff check --fix

testapi:
	@$(MAKE) -C api tests

testapi_unit:
	@$(MAKE) -C api tests_unit
	@$(MAKE) -C api schema_test

testauthorizer:
	cd authorizer; pip install -r requirements-dev.txt; pytest

testall: testapi testauthorizer

testall_unit: testapi_unit testauthorizer
