import subprocess

import typer_cloup as typer
from docs_src.terminating import tutorial003 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_cli():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "New user created: Camila" in result.output


def test_root():
    result = runner.invoke(app, ["root"])
    assert result.exit_code == 1
    assert "The root user is reserved" in result.output
    assert "Aborted!" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
