# justfile
run:
    uv run python src/main.py

test:
    uv run pytest

lint:
    uv run ruff check .

add pkg:
    uv add {{pkg}}
