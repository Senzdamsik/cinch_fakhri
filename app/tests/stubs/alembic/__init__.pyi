"""Type stubs for alembic."""

from __future__ import annotations

from alembic.config import Config

class Command:
    @staticmethod
    def upgrade(
        config: Config, revision: str, sql: bool = False, tag: str | None = None
    ) -> None: ...
    @staticmethod
    def downgrade(
        config: Config, revision: str, sql: bool = False, tag: str | None = None
    ) -> None: ...
