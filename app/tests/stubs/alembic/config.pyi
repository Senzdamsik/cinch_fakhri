"""Type stubs for alembic.config."""

class Config:
    def __init__(
        self,
        file_: str,
        ini_section: str = ...,
        cmd_opts: object | None = ...,
        config_args: dict | None = ...,
    ) -> None: ...
