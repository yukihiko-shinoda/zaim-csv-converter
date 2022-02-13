# type: ignore
"""Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
# Reason: invoke doesn't seem to support type hint, otherwise commands cause error:
# ValueError: Function has keyword-only parameters or annotations,
# use inspect.signature() API which can support them
from pathlib import Path
import platform
import shutil
import webbrowser

from invoke.runners import Failure, Result
from invoke import task

ROOT_DIR = Path(__file__).parent
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("zaimcsvconverter")
TASKS_PY = ROOT_DIR.joinpath("tasks.py")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [TASKS_PY, SOURCE_DIR, TEST_DIR]]


def _delete_file(file):
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        try:
            file.unlink()
        except FileNotFoundError:
            pass


@task(help={"check": "Checks if source is formatted without applying changes"})
def style(context, check=False):
    """Formats code."""
    for result in [
        docformatter(context, check),
        isort(context, check),
        autoflake(context, check),
        black(context, check),
    ]:
        if result.failed:
            raise Failure(result)


@task
def docformatter(context, check=False):
    """Runs docformatter.

    This function includes hard coding of line length.
    see:
    - Add pyproject.toml support for config (Issue #10) by weibullguy · Pull Request #77 · PyCQA/docformatter
      https://github.com/PyCQA/docformatter/pull/77
    """
    list_options = ["--recursive", "--wrap-summaries", "119", "--wrap-descriptions", "119"]
    if check:
        list_options.append("--check")
    else:
        list_options.append("--in-place")
    docformatter_options = f"{' '.join(list_options)}"
    return context.run(f"docformatter {docformatter_options} {' '.join(PYTHON_DIRS)}", warn=True)


def autoflake(context, check=False) -> Result:
    """Runs autoflake."""
    autoflake_options = f"{'--recursive'} {'--check' if check else '--in-place'}"
    return context.run(f"autoflake {autoflake_options} {' '.join(PYTHON_DIRS)}", warn=True)


def isort(context, check=False) -> Result:
    """Runs isort."""
    isort_options = "--check-only --diff" if check else ""
    space = " "
    return context.run(f"isort {isort_options} {space.join(PYTHON_DIRS)}", warn=True)


def black(context, check=False) -> Result:
    """Runs black."""
    black_options = "--check --diff" if check else ""
    space = " "
    return context.run(f"black {black_options} {space.join(PYTHON_DIRS)}", warn=True)


@task
def lint_flake8(context):
    """Lints code with flake8."""
    space = " "
    context.run(f"flake8 --radon-show-closures {space.join(PYTHON_DIRS)}")


@task
def lint_pylint(context):
    """Lints code with pylint."""
    space = " "
    context.run(f"pylint {space.join(PYTHON_DIRS)}")


@task
def lint_mypy(context):
    """Lints code with pylint."""
    space = " "
    context.run(f"mypy {space.join(PYTHON_DIRS)}")


@task
def lint_bandit(context):
    """Lints code with bandit."""
    space = " "
    context.run(f"bandit --recursive {space.join([str(p) for p in [SOURCE_DIR, TASKS_PY]])}", pty=True)
    context.run(f"bandit --recursive --skip B101 {TEST_DIR}", pty=True)


@task
def lint_dodgy(context):
    """Lints code with dodgy."""
    context.run("dodgy --ignore-paths csvinput", pty=True)


@task
def lint_pydocstyle(context):
    """Lints code with pydocstyle."""
    context.run("pydocstyle .", pty=True)


@task(lint_bandit, lint_dodgy, lint_flake8, lint_pydocstyle)
def lint(_context):
    """Runs light linting."""


@task(lint_mypy, lint_pylint)
def lint_deep(_context):
    """Runs deep linting."""


@task
def radon_cc(context):
    """Reports code complexity."""
    space = " "
    context.run(f"radon cc {space.join(PYTHON_DIRS)}")


@task
def radon_mi(context):
    """Reports maintainability index."""
    space = " "
    context.run(f"radon mi {space.join(PYTHON_DIRS)}")


@task(radon_cc, radon_mi)
def radon(_context):
    """Reports radon."""


@task
def xenon(context):
    """Checks code complexity."""
    space = " "
    context.run(("xenon" " --max-absolute A" "--max-modules A" "--max-average A" f"{space.join(PYTHON_DIRS)}"))


@task
def cohesion(context):
    """Lints code with Cohesion."""
    # 2021-10-24:
    # Cohension doesn't support multiple directories in 1 command.
    # Only the last directory enables when supply multiple --directory options.
    context.run(f"cohesion --directory {SOURCE_DIR}", pty=True)
    context.run(f"cohesion --directory {TEST_DIR}", pty=True)


@task
def test(context):
    """Runs tests."""
    pty = platform.system() == "Linux"
    context.run("pytest -v", pty=pty)


@task(help={"publish": "Publish the result via coveralls", "xml": "Export report as xml format"})
def coverage(context, publish=False, xml=False):
    """Creates coverage report."""
    pty = platform.system() == "Linux"
    context.run("coverage run --concurrency=multiprocessing -m pytest", pty=pty)
    context.run("coverage combine", pty=pty)
    context.run("coverage report --show-missing", pty=pty)
    if publish:
        # Publish the results via coveralls
        context.run("coveralls", pty=pty)
        return
    # Build a local report
    if xml:
        context.run("coverage xml", pty=pty)
    else:
        context.run("coverage html", pty=pty)
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task
def clean_build(context):
    """Cleans up files from package building."""
    context.run("rm -fr build/")
    context.run("rm -fr dist/")
    context.run("rm -fr .eggs/")
    context.run("find . -name '*.egg-info' -exec rm -fr {} +")
    context.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(context):
    """Cleans up python file artifacts."""
    context.run("find . -name '*.pyc' -exec rm -f {} +")
    context.run("find . -name '*.pyo' -exec rm -f {} +")
    context.run("find . -name '*~' -exec rm -f {} +")
    context.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(_context):
    """Cleans up files from testing."""
    _delete_file(COVERAGE_FILE)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests])
def clean(_context):
    """Runs all clean sub-tasks."""


@task(clean)
def dist(context):
    """Builds source and wheel packages."""
    context.run("python setup.py sdist")
    context.run("python setup.py bdist_wheel")
