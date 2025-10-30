FROM futureys/claude-code-python-development:20251026170000
COPY pyproject.toml uv.lock /workspace/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --python=3.13
COPY . /workspace
ENTRYPOINT [ "uv", "run" ]
CMD ["convert.py"]
