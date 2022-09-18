# Slim image can't install numpy
FROM python:3.10.7-bullseye as production
WORKDIR /workspace
COPY Pipfile Pipfile.lock /workspace/
RUN pip --no-cache-dir install pipenv \
 && pipenv install --deploy --system \
 && pip uninstall -y pipenv virtualenv-clone virtualenv
COPY . /workspace

ENTRYPOINT [ "python3", "convert.py" ]

FROM production as development
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip --no-cache-dir install pipenv \
 && pipenv sync --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
