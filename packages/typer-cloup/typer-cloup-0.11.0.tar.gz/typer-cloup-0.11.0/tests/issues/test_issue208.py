import typer_cloup as typer
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = typer.Typer(
    context_settings=dict(
        help_option_names=["-h", "--help"],
    )
)


@app.command()
def main():
    pass  # pragma: no cover


def test_help_short_option():
    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
