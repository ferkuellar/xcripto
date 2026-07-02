from pathlib import Path

from alembic.config import Config


def test_alembic_config_is_present_and_points_to_backend_migrations():
    config_path = Path("alembic.ini")
    config = Config(config_path)

    assert config_path.exists()
    assert config.get_main_option("script_location") == "alembic"


def test_initial_alembic_migration_exists():
    migration_path = Path("alembic/versions/20260702_0001_initial_schema.py")
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "news_items" in migration_text
    assert "source_references" in migration_text
    assert "agent_executions" in migration_text
    assert "audit_checks" in migration_text
