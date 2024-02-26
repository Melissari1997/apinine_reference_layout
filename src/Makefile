format:
	@ruff check

fix-format:
	@ruff check --fix

testapi:
	@$(MAKE) -C api tests

testauthorizer:
	pytest authorizer

testall: testapi testauthorizer
