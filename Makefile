.PHONY: test

test:
	@py.test --cov --cov-report term-missing
	@coverage html

clean:
	find . -name "__pycache__" -exec rm -rf {} \;
	rm -rf htmlcov
