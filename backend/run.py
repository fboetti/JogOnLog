# Backend Requirements Imports -- #
import typing

import typer
import uvicorn
# -- Backend Package Imports -- #
from src.run import (
    handle_make_migrations,
    handle_upgrade_migrations,
    handle_downgrade_migrations,
)

typer_app = typer.Typer()


@typer_app.command()
def alembic(
        upgrade: bool = typer.Option(False),
        downgrade: bool = typer.Option(False),
        make: bool = typer.Option(False),
        revision: typing.Optional[str] = typer.Option(None),
        make_message: typing.Optional[str] = typer.Option(None),
) -> None:
    """
    Run the alembic command line tool.
    """
    if make:
        handle_make_migrations(message=make_message)
        print("✅  Migration file created!")

    if upgrade:
        handle_upgrade_migrations(revision=revision)
        print("✅  Upgrade Done!")

    if downgrade:
        handle_downgrade_migrations(revision=revision)
        print("✅  Downgrade Done!")


@typer_app.command()
def run(
        reload: bool = typer.Option(False),
        run_migrations: bool = typer.Option(False),
) -> None:
    """
    If run_migrations is set to True, runs the alembic migrations to latest version.
    Then starts the FastAPI application.
    """
    try:
        if run_migrations:
            print("📈 Running migrations upgrade...")
            handle_upgrade_migrations()
    except Exception as e:
        print(f"❌  Error running migrations: {e}")

    print("🚀 Starting backend...")
    uvicorn.run(
        app="src.main:app",
        reload=reload,
        host="0.0.0.0",
        timeout_keep_alive=10,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    typer_app()
