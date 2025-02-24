test:
	@echo "Running tests"
	pytest tests/

clean:
	@echo "Cleaning up"
	rm -rf app/__pycache__/
	rm -rf tests/__pycache__/