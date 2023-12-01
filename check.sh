ruff check --fix-only --unsafe-fixes . \
    && ruff format . \
    && mypy . \
    && ruff check . \
