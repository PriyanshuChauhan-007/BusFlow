.PHONY: install test lint run compose-up compose-down

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

lint:
	python -m ruff check .

run:
	python -m uvicorn busflow.main:app --reload

compose-up:
	docker compose up --build

compose-down:
	docker compose down
