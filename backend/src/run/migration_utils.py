# -- Pure Python Imports -- #
import typing
# -- Backend Requirements Imports -- #
import alembic.config
from alembic.script import ScriptDirectory

__all__ = [
    "handle_make_migrations",
    "handle_upgrade_migrations",
    "handle_downgrade_migrations",
]


# -- Private Methods -- #

def _merge_procedure(
        head_revisions_ids: typing.List[str],
) -> None:
    """
    Merge multiple heads detected in the alembic history.
    """
    print("\n🔍 Multiple heads detected! Running the merge procedure...")

    merge_argv = [
        "merge",
        *head_revisions_ids,
        "-m",
        f"merge {' and '.join(head_revisions_ids)}",
    ]
    alembic.config.main(argv=merge_argv)


# -- Exposed Methods -- #

def handle_make_migrations(
        message: typing.Optional[str] = None,
) -> None:
    """
    Alembic "make" command that creates a new migration file in alembic/versions folder.
    """
    print("\n📦  Generating Migrations  📦\n")
    make_argv = [
        "--raiseerr",
        "revision",
        "--autogenerate",
    ]
    if message:
        make_argv.extend(["-m", message])

    alembic.config.main(argv=make_argv)


def handle_upgrade_migrations(
        revision: str = "head",
) -> None:
    """
    Runs alembic migrations to latest version available if no revision is specified.
    Otherwise, runs alembic migrations-upgrade until the specified revision.
    """
    # Check multiple heads and, if so, merge them in one single revision file before the upgrade operation.
    alembic_cfg = alembic.config.Config("alembic.ini")
    script_dir = ScriptDirectory.from_config(alembic_cfg)
    head_revisions_ids = script_dir.get_heads()
    if len(head_revisions_ids) > 1:
        _merge_procedure(head_revisions_ids)

    print(f"\n📈  Migrations: upgrading to revision {revision}  📈\n")
    upgrade_argv = [
        "--raiseerr",
        "upgrade",
        revision,
    ]

    alembic.config.main(argv=upgrade_argv)


def handle_downgrade_migrations(
        revision: str = "-1",
) -> None:
    """
    Runs alembic migrations downgrade to the previous version if no revision is specified.
    Otherwise, runs alembic migration-downgrade until the specified revision.
    """
    print(f"\n📉  Migrations: downgrading to revision {revision}  📉\n")
    downgrade_argv = [
        "downgrade",
        revision,
    ]

    alembic.config.main(argv=downgrade_argv)
