FROM python:3.13.5-slim-bookworm
WORKDIR /workspace
# Using uv in Docker | uv
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.7.20 /uv /uvx /bin/
# - Using uv in Docker | uv
#.  https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy
# The uv command also errors out when installing semgrep:
# - Getting semgrep-core in pipenv · Issue #2929 · semgrep/semgrep
#   https://github.com/semgrep/semgrep/issues/2929#issuecomment-818994969
ENV SEMGREP_SKIP_BIN=true
COPY pyproject.toml uv.lock /workspace/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
COPY . /workspace
ENTRYPOINT [ "uv", "run" ]
CMD ["convert.py"]
