webapi:
	@pipenv run pip freeze > requirements.txt
	@docker-compose up -d --build
	@rm requirements.txt

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

test:
	@pytest

test-match:
	@pytest -k ${Q}

test-coverage:
	@pytest --cov wishlist

lint:
	@isort . --check
	@autopep8 . -r --diff

format:
	@isort .
	@autopep8 . -r --in-place

safety:
	@safety check
