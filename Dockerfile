FROM futureys/claude-code-python-development:20260710125000
# To prevent following error when install semgrep:
# 8.445       error: command 'cc' failed: No such file or directory
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock /workspace/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
COPY . /workspace
ENTRYPOINT [ "uv", "run" ]
CMD ["convert.py"]
