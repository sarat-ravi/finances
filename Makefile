default:
	@echo "USAGE"
	@echo "------------------------------------"
	@echo "test - run all the tests."

.PHONY: test
test:
	nosetests
