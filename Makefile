webapi:
	@docker-compose up -d

webapi-dev:
	@uvicorn --reload wishlist.webapi:app

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@find . -name "*.cache" -type d | xargs rm -rf
	@find . -name "*htmlcov" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f coverage.xml

lint:
	@isort . --check
	@autopep8 . -r --diff

format:
	@isort .
	@autopep8 . -r --in-place

safety:
	@pipenv check
