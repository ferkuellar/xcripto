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


def test_editorial_core_alembic_migration_exists():
    migration_path = Path("alembic/versions/20260702_0002_add_editorial_core_entities.py")
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "verification_records" in migration_text
    assert "risk_reviews" in migration_text
    assert "content_pieces" in migration_text
    assert "distribution_plans" in migration_text
    assert "publication_records" in migration_text


def test_workflow_orchestration_alembic_migration_exists():
    migration_path = Path("alembic/versions/20260702_0003_add_workflow_orchestration.py")
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "workflow_runs" in migration_text
    assert "workflow_steps" in migration_text
