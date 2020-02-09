import typer
import webbrowser
import subprocess

from pathlib import Path
from functools import wraps

app = typer.Typer()


def typer_cli(f):
    # @app.command() does not work, dunno why
    @wraps(f)
    def wrapper():
        return typer.run(f)

    return wrapper


def print_styled_command(command):
    typer.echo(
        typer.style(
            "Running command line:",
            fg=typer.colors.WHITE,
            bg=typer.colors.GREEN,
            bold=True,
        )
    )
    typer.echo(typer.style(" ".join(command), bold=True) + "\n")


def run_command(command, debug=False, cwd=None):
    command = command.split()
    if debug:
        print_styled_command(command)
    subprocess.run(command, cwd=cwd)


@typer_cli
def test(test_path: str = typer.Argument(None)):
    command = "python runtests.py tests"
    if test_path is not None:
        command = f"{command} {test_path}"
    run_command(command, debug=True)


@typer_cli
def pytest(test_path: str = typer.Argument(None)):
    command = "pytest"
    if test_path is not None:
        command = f"{command} {test_path}"
    run_command(command, debug=True)


@typer_cli
def flake8():
    command = "flake8 src tests"
    run_command(command, debug=True)


@typer_cli
def black():
    command = "black src tests"
    run_command(command, debug=True)


@typer_cli
def coverage():
    commands = [
        "coverage run --source src runtests.py tests",
        "coverage report -m",
        "coverage html",
    ]
    for command in commands:
        run_command(command, debug=True)
    file_url = "file://" + str(Path("htmlcov/index.html").resolve())
    webbrowser.open_new_tab(file_url)


@typer_cli
def docs():
    Path("docs/modules.rst").unlink(missing_ok=True)
    Path("docs/wagtail_srcset.rst").unlink(missing_ok=True)
    commands = [
        "sphinx-apidoc -o docs/ src/wagtail_srcset",
        "make -C docs clean",
        "make -C docs html",
    ]
    for command in commands:
        run_command(command, debug=True)
    file_url = "file://" + str(Path("docs/_build/html/index.html").resolve())
    webbrowser.open_new_tab(file_url)


@typer_cli
def notebook():
    command = "python ../manage.py shell_plus --notebook"
    run_command(command, cwd="notebooks", debug=True)
