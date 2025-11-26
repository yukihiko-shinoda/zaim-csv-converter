FROM futureys/claude-code-python-development:20251104123000
COPY pyproject.toml uv.lock /workspace/
RUN apt-get update && apt-get install -y --no-install-recommends \
    # To install radon from GitHub source
    git/stable \
    && rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --python=3.13
COPY . /workspace
ENTRYPOINT [ "uv", "run" ]
CMD ["convert.py"]
