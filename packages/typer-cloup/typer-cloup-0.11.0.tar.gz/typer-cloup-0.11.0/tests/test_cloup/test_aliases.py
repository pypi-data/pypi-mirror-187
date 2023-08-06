import click

import typer_cloup as typer
from typer_cloup.testing import CliRunner, columns_match

runner = CliRunner()

app = typer.Typer(show_subcommand_aliases=True)


@app.callback()
def callback():
    """A package installer."""


@app.command(aliases=["i", "add"])
def install(pkg: str):
    """Install a package."""
    typer.echo(f"install: {pkg}")


# Aliases works even if cls is not a Cloup command class
@app.command(aliases=["uni", "rm"], cls=click.Command)
def uninstall(pkg: str):
    """Uninstall a package."""
    typer.echo(f"uninstall: {pkg}")


def test_help():
    result = runner.invoke(app, ["--help"])
    print(result.output)
    assert result.exit_code == 0
    assert "A package installer." in result.output
    assert columns_match(result.output, "install (i, add)", "Install a package.")
    assert columns_match(result.output, "uninstall (uni, rm)", "Uninstall a package.")


def test_install():
    result = runner.invoke(app, ["install", "foo"])
    assert result.exit_code == 0
    assert "install: foo" in result.output


def test_i():
    result = runner.invoke(app, ["i", "foo"])
    assert result.exit_code == 0
    assert "install: foo" in result.output


def test_add():
    result = runner.invoke(app, ["add", "foo"])
    assert result.exit_code == 0
    assert "install: foo" in result.output


def test_uninstall():
    result = runner.invoke(app, ["uninstall", "foo"])
    assert result.exit_code == 0
    assert "uninstall: foo" in result.output


def test_uni():
    result = runner.invoke(app, ["uni", "foo"])
    assert result.exit_code == 0
    assert "uninstall: foo" in result.output


def test_rm():
    result = runner.invoke(app, ["rm", "foo"])
    assert result.exit_code == 0
    assert "uninstall: foo" in result.output


def test_group():
    app = typer.Typer(show_subcommand_aliases=True)
    foo_app = typer.Typer(name="foo", aliases=["bar"], show_subcommand_aliases=True)

    app.add_sub(foo_app)

    @foo_app.command()
    def main():
        typer.echo("Hello World")

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "foo (bar)" in result.stdout

    result = runner.invoke(app, ["foo", "main"])
    assert result.exit_code == 0
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["bar", "main"])
    assert result.exit_code == 0
    assert "Hello World" in result.stdout
