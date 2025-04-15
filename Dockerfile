# Slim image can't install numpy
FROM python:3.13.3-slim-bookworm AS production
WORKDIR /workspace
# setuptools 65.3.0 can't lock package defined its dependencies by pyproject.toml
RUN pip install --no-cache-dir --upgrade setuptools>=65.4.0
ENV UV_PROJECT_ENVIRONMENT=/usr/local/
COPY pyproject.toml uv.lock /workspace/
RUN pip install --no-cache-dir uv==0.6.14 \
 && uv sync --no-dev \
 && uv cache clean \
 && pip uninstall -y uv
COPY . /workspace
ENTRYPOINT [ "python3", "convert.py" ]

FROM production AS development
ENV UV_PROJECT_ENVIRONMENT=
# The uv command also errors out when installing semgrep:
# - Getting semgrep-core in pipenv · Issue #2929 · semgrep/semgrep
#   https://github.com/semgrep/semgrep/issues/2929#issuecomment-818994969
ENV SEMGREP_SKIP_BIN=true
RUN pip install --no-cache-dir uv===0.6.14
# Reason: This is not for production
# hadolint ignore=DL3059
RUN uv sync
ENTRYPOINT [ "uv", "run" ]
CMD ["pytest"]
