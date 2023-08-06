from typing import Optional

from cloup.constraints import RequireAtLeast, mutually_exclusive

import typer_cloup as typer
from typer_cloup import option_group
from typer_cloup.testing import CliRunner, columns_match

runner = CliRunner()

app = typer.Typer()


@app.command()
@option_group(
    "Cool options",
    "foo",
    "bar",
    constraint=mutually_exclusive,
)
@option_group(
    "Other cool options",
    "pippo",
    "pluto",
    constraint=RequireAtLeast(1),
    help="This is the optional description of this option group.",
)
def main(
    foo: str = typer.Option(None, help="This text should describe the option --foo."),
    bar: str = typer.Option(None, help="This text should describe the option --bar."),
    pippo: str = typer.Option(
        None, help="This text should describe the option --pippo."
    ),
    pluto: str = typer.Option(
        None, help="This text should describe the option --pluto."
    ),
):
    """This is the command description."""
    typer.echo(f"foo: {foo}")
    typer.echo(f"bar: {bar}")
    typer.echo(f"pippo: {pippo}")
    typer.echo(f"pluto: {pluto}")


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS]" in result.output
    assert "This is the command description." in result.output
    assert "Cool options: [mutually exclusive]" in result.output
    assert columns_match(
        result.output, "--foo TEXT", "This text should describe the option --foo."
    )
    assert columns_match(
        result.output, "--bar TEXT", "This text should describe the option --bar."
    )
    assert "Other cool options: [at least 1 required]" in result.output
    assert "This is the optional description of this option group." in result.output
    assert columns_match(
        result.output, "--pippo TEXT", "This text should describe the option --pippo."
    )
    assert columns_match(
        result.output, "--pluto TEXT", "This text should describe the option --pluto."
    )


def test_output():
    result = runner.invoke(
        app, ["--foo", "foo", "--pippo", "pippo", "--pluto", "pluto"]
    )
    assert result.exit_code == 0
    assert "foo: foo" in result.output
    assert "bar: None" in result.output
    assert "pippo: pippo" in result.output
    assert "pluto: pluto" in result.output


def test_too_many_options():
    result = runner.invoke(app, ["--foo", "foo", "--bar", "bar"])
    assert result.exit_code != 0
    assert "Error: the following parameters are mutually exclusive:" in result.output
    assert "--foo" in result.output
    assert "--bar" in result.output


def test_too_few_options():
    result = runner.invoke(app, [])
    assert result.exit_code != 0
    assert "Error: at least 1 of the following parameters must be set:" in result.output
    assert "--pippo" in result.output
    assert "--pluto" in result.output


def test_help_hidden_group():
    app = typer.Typer()

    @app.command()
    @option_group("Some group", "foo", hidden=True)
    def main(foo: Optional[str] = typer.Option(None)):
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Some group" not in result.stdout
    assert "--foo" not in result.stdout
