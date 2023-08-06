import subprocess

import typer_cloup as typer
from docs_src.parameter_types.bool import tutorial003 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "-f, --force / -F, --no-force" in result.output


def test_force():
    result = runner.invoke(app, ["-f"])
    assert result.exit_code == 0
    assert "Forcing operation" in result.output


def test_no_force():
    result = runner.invoke(app, ["-F"])
    assert result.exit_code == 0
    assert "Not forcing" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
