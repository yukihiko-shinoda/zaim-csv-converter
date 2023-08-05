# Slim image can't install numpy
FROM python:3.11.4-bookworm as production
WORKDIR /workspace
# setuptools 65.3.0 can't lock package defined its dependencies by pyproject.toml
RUN pip install --upgrade setuptools>=65.4.0
COPY Pipfile Pipfile.lock /workspace/
# see:
# - Fail to pipenv update due to MetadataGenerationFailed · Issue #5377 · pypa/pipenv
#   https://github.com/pypa/pipenv/issues/5377
RUN pip --no-cache-dir install pipenv==2023.7.23 \
 && pipenv install --deploy --system \
 && pip uninstall -y pipenv virtualenv-clone virtualenv
COPY . /workspace

ENTRYPOINT [ "python3", "convert.py" ]

FROM production as development
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
# see:
# - Fail to pipenv update due to MetadataGenerationFailed · Issue #5377 · pypa/pipenv
#   https://github.com/pypa/pipenv/issues/5377
RUN pip --no-cache-dir install pipenv==2023.7.23 \
 && pipenv sync --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
