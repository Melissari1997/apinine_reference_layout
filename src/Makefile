.PHONY: wildfire all format tests


all:
	echo "Calling all makefiles"
	@$(MAKE) -C wildfire

wildfire:
	@$(MAKE) -C wildfire

tests:
	for risk in "wildfire"; do \
		$(MAKE) -C $$risk tests; \
	done

format:
	@ruff check

fix-format:
	@ruff check --fix
