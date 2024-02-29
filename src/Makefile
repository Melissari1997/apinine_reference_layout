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
	pytest authorizer

testall: testapi testauthorizer
