import subprocess

import typer_cloup as typer
from docs_src.parameter_types.enum import tutorial002 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_upper():
    result = runner.invoke(app, ["--network", "CONV"])
    assert result.exit_code == 0
    assert "Training neural network of type: conv" in result.output


def test_mix():
    result = runner.invoke(app, ["--network", "LsTm"])
    assert result.exit_code == 0
    assert "Training neural network of type: lstm" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
