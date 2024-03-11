format:
	@ruff check

fix-format:
	@ruff check --fix

testapi:
	@$(MAKE) -C api tests
	@$(MAKE) -C api schema_test

testapi_unit:
	@$(MAKE) -C api tests_unit
	@$(MAKE) -C api schema_test

testauthorizer:
	cd authorizer; pip install -r requirements-dev.txt; pytest

testcognito_unit:
	@$(MAKE) -C api test_cognito_unit

testcognito:
	@$(MAKE) -C api test_cognito

testall: testapi testauthorizer testcognito

testall_unit: testapi_unit testauthorizer testcognito_unit

docker_risks:
	@$(MAKE) -C api docker_risks

docker_cognito:
	@$(MAKE) -C api docker_cognito
