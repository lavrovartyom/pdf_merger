.PHONY: run test lint clean

run:
	uv run streamlit run app/main.py

test:
	uv run pytest -v --maxfail=1 --disable-warnings

lint:
	uv run ruff check . --fix
	uv run isort .
	uv run black .

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ */__pycache__ .mypy_cache