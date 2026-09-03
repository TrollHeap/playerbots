PYTHON ?= python3
TESTS := $(sort $(wildcard tests/test_*.py))

test:
	@test -n "$(TESTS)"
	@set -e; for test_file in $(TESTS); do $(PYTHON) "$$test_file"; done

.PHONY: test
