"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
import webbrowser
from pathlib import Path

from invoke import Failure, Result, task  # type: ignore

ROOT_DIR = Path(__file__).parent
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("zaimcsvconverter")
TASKS_PY = ROOT_DIR.joinpath("tasks.py")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [TASKS_PY, SOURCE_DIR, TEST_DIR]]


@task(help={"check": "Checks if source is formatted without applying changes"})
def style(context, check=False):
    """
    Format code
    """
    for result in [
        isort(context, check),
        black(context, check),
    ]:
        if result.failed:
            raise Failure(result)


def isort(context, check=False) -> Result:
    """Runs isort."""
    isort_options = "--recursive {}".format("--check-only --diff" if check else "")
    return context.run("isort {} {}".format(isort_options, " ".join(PYTHON_DIRS)), warn=True)


def black(context, check=False) -> Result:
    """Runs black."""
    black_options = "{}".format("--check --diff" if check else "")
    return context.run("black {} {}".format(black_options, " ".join(PYTHON_DIRS)), warn=True)


@task(help={"publish": "Publish the result via coveralls", "xml": "Export report as xml format"})
def coverage(context, publish=False, xml=False):
    """
    Create coverage report
    """
    context.run("coverage run --source {} -m pytest".format(SOURCE_DIR))
    context.run("coverage report")
    if publish:
        # Publish the results via coveralls
        context.run("coveralls")
        return
    # Build a local report
    if xml:
        context.run("coverage xml")
    else:
        context.run("coverage html")
        webbrowser.open(COVERAGE_REPORT.as_uri())