import re
from typing import IO, Any, Mapping, Optional, Sequence, Union

from click.testing import CliRunner as ClickCliRunner  # noqa
from click.testing import Result

from typer_cloup.main import Typer
from typer_cloup.main import get_command as _get_command


class CliRunner(ClickCliRunner):
    def invoke(  # type: ignore
        self,
        app: Typer,
        args: Optional[Union[str, Sequence[str]]] = None,
        input: Optional[Union[bytes, str, IO[Any]]] = None,
        env: Optional[Mapping[str, str]] = None,
        catch_exceptions: bool = True,
        color: bool = False,
        **extra: Any,
    ) -> Result:
        use_cli = _get_command(app)
        return super().invoke(
            use_cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            color=color,
            **extra,
        )


def columns_match(output: str, *cols: str) -> bool:
    pattern = r" *  ".join(re.escape(col) for col in cols)
    return bool(re.search(pattern, output))
