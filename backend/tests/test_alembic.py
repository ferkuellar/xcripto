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


def test_workflow_task_queue_alembic_migration_exists():
    migration_path = Path("alembic/versions/20260702_0005_add_workflow_task_queue.py")
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "workflow_tasks" in migration_text
    assert "ix_workflow_tasks_workflow_run_id" in migration_text
    assert "ix_workflow_tasks_created_at" in migration_text


def test_workflow_orchestration_alembic_migration_exists():
    migration_path = Path("alembic/versions/20260702_0003_add_workflow_orchestration.py")
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "workflow_runs" in migration_text
    assert "workflow_steps" in migration_text


def test_agent_output_storage_alembic_migration_exists():
    migration_path = Path("alembic/versions/20260702_0004_add_agent_output_storage.py")
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "agent_outputs" in migration_text


def test_metrics_memory_knowledge_alembic_migration_exists():
    migration_path = Path("alembic/versions/20260702_0006_add_metrics_memory_knowledge_core.py")
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "metric_snapshots" in migration_text
    assert "memory_items" in migration_text
    assert "knowledge_nodes" in migration_text
    assert "knowledge_edges" in migration_text


def test_editorial_readiness_alembic_migration_exists():
    migration_path = Path("alembic/versions/20260702_0007_add_editorial_readiness_scores.py")
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "editorial_readiness_scores" in migration_text
    assert "ix_editorial_readiness_scores_news_item_id" in migration_text
    assert "ix_editorial_readiness_scores_score_band" in migration_text


def test_intake_alembic_migration_exists():
    migration_path = Path(
        "alembic/versions/20260702_0008_add_intake_adapters_and_deduplication.py"
    )
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "intake_signals" in migration_text
    assert "intake_adapter_runs" in migration_text
    assert "ix_intake_signals_content_hash" in migration_text
    assert "ix_intake_adapter_runs_adapter_name" in migration_text


def test_rbac_alembic_migration_exists():
    migration_path = Path("alembic/versions/20260702_0009_add_users_roles_and_ownership.py")
    migration_text = migration_path.read_text(encoding="utf-8")

    assert migration_path.exists()
    assert "user_accounts" in migration_text
    assert "ownership_assignments" in migration_text
    assert "ix_user_accounts_role" in migration_text
    assert "ix_ownership_assignments_entity_type" in migration_text
