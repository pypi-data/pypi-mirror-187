import subprocess

import typer_cloup as typer
from docs_src.prompt import tutorial003 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_cli():
    result = runner.invoke(app, input="y\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete it? [y/N]:" in result.output
    assert "Deleting it!" in result.output


def test_no_confirm():
    result = runner.invoke(app, input="n\n")
    assert result.exit_code == 1
    assert "Are you sure you want to delete it? [y/N]:" in result.output
    assert "Aborted!" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
