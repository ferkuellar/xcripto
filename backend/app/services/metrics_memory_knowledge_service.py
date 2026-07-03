from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import AUTO_REVIEW_MEMORY_TYPES
from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.models import (
    AgentExecution,
    AgentOutput,
    AuditCheck,
    ContentPiece,
    DistributionPlan,
    KnowledgeEdge,
    KnowledgeNode,
    MemoryItem,
    MetricSnapshot,
    NewsItem,
    PublicationRecord,
    WorkflowRun,
    WorkflowTask,
)
from app.schemas.knowledge import KnowledgeEdgeCreate, KnowledgeNodeCreate
from app.schemas.memory_item import MemoryItemCreate
from app.schemas.metric_snapshot import MetricSnapshotCreate


async def create_metric_snapshot(
    session: AsyncSession,
    payload: MetricSnapshotCreate,
    correlation_id: str | None = None,
) -> MetricSnapshot:
    await _validate_metric_relations(session, payload)
    snapshot = MetricSnapshot(**payload.model_dump())
    if snapshot.correlation_id is None:
        snapshot.correlation_id = correlation_id
    session.add(snapshot)
    await session.commit()
    await session.refresh(snapshot)
    return snapshot


async def list_metric_snapshots(
    session: AsyncSession,
    entity_type: str | None = None,
    entity_id: str | None = None,
    news_item_id: str | None = None,
    content_piece_id: str | None = None,
    distribution_plan_id: str | None = None,
    publication_record_id: str | None = None,
    workflow_run_id: str | None = None,
    workflow_task_id: str | None = None,
    agent_execution_id: str | None = None,
    agent_output_id: str | None = None,
    metric_category: str | None = None,
    channel: str | None = None,
    measurement_window: str | None = None,
    metric_name: str | None = None,
    data_quality: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[MetricSnapshot]:
    stmt = select(MetricSnapshot).order_by(MetricSnapshot.created_at.desc())
    filters = {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "news_item_id": news_item_id,
        "content_piece_id": content_piece_id,
        "distribution_plan_id": distribution_plan_id,
        "publication_record_id": publication_record_id,
        "workflow_run_id": workflow_run_id,
        "workflow_task_id": workflow_task_id,
        "agent_execution_id": agent_execution_id,
        "agent_output_id": agent_output_id,
        "metric_category": metric_category,
        "channel": channel,
        "measurement_window": measurement_window,
        "metric_name": metric_name,
        "data_quality": data_quality,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(MetricSnapshot, column_name) == value)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_metric_snapshot(session: AsyncSession, metric_snapshot_id: str) -> MetricSnapshot:
    snapshot = await session.get(MetricSnapshot, metric_snapshot_id)
    if snapshot is None:
        raise NotFoundError("Metric snapshot")
    return snapshot


async def create_memory_item(
    session: AsyncSession,
    payload: MemoryItemCreate,
    correlation_id: str | None = None,
) -> MemoryItem:
    await _validate_memory_relations(session, payload)
    data = payload.model_dump()
    if data["memory_type"] in AUTO_REVIEW_MEMORY_TYPES and not data["human_review_required"]:
        data["human_review_required"] = True
    memory = MemoryItem(**data)
    if memory.correlation_id is None:
        memory.correlation_id = correlation_id
    session.add(memory)
    await session.commit()
    await session.refresh(memory)
    return memory


async def list_memory_items(
    session: AsyncSession,
    memory_type: str | None = None,
    memory_status: str | None = None,
    scope: str | None = None,
    confidence_level: str | None = None,
    persistence_level: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    news_item_id: str | None = None,
    workflow_run_id: str | None = None,
    agent_output_id: str | None = None,
    human_review_required: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[MemoryItem]:
    stmt = select(MemoryItem).order_by(MemoryItem.created_at.desc())
    filters = {
        "memory_type": memory_type,
        "memory_status": memory_status,
        "scope": scope,
        "confidence_level": confidence_level,
        "persistence_level": persistence_level,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "news_item_id": news_item_id,
        "workflow_run_id": workflow_run_id,
        "agent_output_id": agent_output_id,
        "human_review_required": human_review_required,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(MemoryItem, column_name) == value)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_memory_item(session: AsyncSession, memory_item_id: str) -> MemoryItem:
    memory = await session.get(MemoryItem, memory_item_id)
    if memory is None:
        raise NotFoundError("Memory item")
    return memory


async def approve_memory_item(
    session: AsyncSession, memory_item_id: str, approved_by: str
) -> MemoryItem:
    memory = await get_memory_item(session, memory_item_id)
    if memory.memory_status == "invalidated":
        raise ConflictError("Invalidated memory cannot be approved")
    memory.memory_status = "approved"
    memory.approved_by = approved_by
    memory.approved_at = datetime.now(UTC)
    memory.invalidated_by = None
    memory.invalidated_at = None
    memory.invalidation_reason = None
    await session.commit()
    await session.refresh(memory)
    return memory


async def reject_memory_item(
    session: AsyncSession, memory_item_id: str, reason: str
) -> MemoryItem:
    memory = await get_memory_item(session, memory_item_id)
    if memory.memory_status == "archived":
        raise ConflictError("Archived memory cannot be rejected")
    memory.memory_status = "rejected"
    memory.invalidation_reason = reason
    await session.commit()
    await session.refresh(memory)
    return memory


async def invalidate_memory_item(
    session: AsyncSession,
    memory_item_id: str,
    invalidated_by: str,
    reason: str,
) -> MemoryItem:
    memory = await get_memory_item(session, memory_item_id)
    if memory.memory_status == "archived":
        raise ConflictError("Archived memory cannot be invalidated")
    memory.memory_status = "invalidated"
    memory.invalidated_by = invalidated_by
    memory.invalidated_at = datetime.now(UTC)
    memory.invalidation_reason = reason
    await session.commit()
    await session.refresh(memory)
    return memory


async def archive_memory_item(
    session: AsyncSession, memory_item_id: str, reason: str | None = None
) -> MemoryItem:
    memory = await get_memory_item(session, memory_item_id)
    if memory.memory_status == "archived":
        return memory
    memory.memory_status = "archived"
    if reason is not None:
        memory.invalidation_reason = reason
    await session.commit()
    await session.refresh(memory)
    return memory


async def create_knowledge_node(
    session: AsyncSession,
    payload: KnowledgeNodeCreate,
    correlation_id: str | None = None,
) -> KnowledgeNode:
    node = KnowledgeNode(**payload.model_dump())
    if node.correlation_id is None:
        node.correlation_id = correlation_id
    session.add(node)
    await session.commit()
    await session.refresh(node)
    return node


async def list_knowledge_nodes(
    session: AsyncSession,
    node_type: str | None = None,
    status: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    confidence_level: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[KnowledgeNode]:
    stmt = select(KnowledgeNode).order_by(KnowledgeNode.created_at.desc())
    filters = {
        "node_type": node_type,
        "status": status,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "confidence_level": confidence_level,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(KnowledgeNode, column_name) == value)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_knowledge_node(session: AsyncSession, node_id: str) -> KnowledgeNode:
    node = await session.get(KnowledgeNode, node_id)
    if node is None:
        raise NotFoundError("Knowledge node")
    return node


async def create_knowledge_edge(
    session: AsyncSession,
    payload: KnowledgeEdgeCreate,
    correlation_id: str | None = None,
) -> KnowledgeEdge:
    await _validate_knowledge_edge(session, payload)
    edge = KnowledgeEdge(**payload.model_dump())
    if edge.correlation_id is None:
        edge.correlation_id = correlation_id
    session.add(edge)
    await session.commit()
    await session.refresh(edge)
    return edge


async def list_knowledge_edges(
    session: AsyncSession,
    source_node_id: str | None = None,
    target_node_id: str | None = None,
    relationship_type: str | None = None,
    scope: str | None = None,
    status: str | None = None,
    confidence_level: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[KnowledgeEdge]:
    stmt = select(KnowledgeEdge).order_by(KnowledgeEdge.created_at.desc())
    filters = {
        "source_node_id": source_node_id,
        "target_node_id": target_node_id,
        "relationship_type": relationship_type,
        "scope": scope,
        "status": status,
        "confidence_level": confidence_level,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(KnowledgeEdge, column_name) == value)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_knowledge_edge(session: AsyncSession, edge_id: str) -> KnowledgeEdge:
    edge = await session.get(KnowledgeEdge, edge_id)
    if edge is None:
        raise NotFoundError("Knowledge edge")
    return edge


async def list_knowledge_edges_for_node(
    session: AsyncSession, node_id: str, limit: int = 50, offset: int = 0
) -> list[KnowledgeEdge]:
    stmt = (
        select(KnowledgeEdge)
        .where(
            (KnowledgeEdge.source_node_id == node_id)
            | (KnowledgeEdge.target_node_id == node_id)
        )
        .order_by(KnowledgeEdge.created_at.desc())
    )
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_knowledge_entity_graph(
    session: AsyncSession, entity_type: str, entity_id: str
) -> dict[str, list]:
    nodes = await list_knowledge_nodes(session, entity_type=entity_type, entity_id=entity_id)
    if not nodes:
        return {"nodes": [], "edges": []}
    node_ids = [node.id for node in nodes]
    stmt = select(KnowledgeEdge).where(
        (KnowledgeEdge.source_node_id.in_(node_ids)) | (KnowledgeEdge.target_node_id.in_(node_ids))
    )
    result = await session.execute(stmt.order_by(KnowledgeEdge.created_at.desc()))
    return {"nodes": nodes, "edges": list(result.scalars().all())}


async def _validate_metric_relations(session: AsyncSession, payload: MetricSnapshotCreate) -> None:
    if payload.entity_type and not payload.entity_id:
        raise DomainValidationError("entity_type and entity_id must be provided together")
    if payload.entity_id and not payload.entity_type:
        raise DomainValidationError("entity_type and entity_id must be provided together")
    if not any(
        [
            payload.entity_type and payload.entity_id,
            payload.news_item_id,
            payload.content_piece_id,
            payload.distribution_plan_id,
            payload.publication_record_id,
            payload.workflow_run_id,
            payload.workflow_task_id,
            payload.agent_execution_id,
            payload.agent_output_id,
        ]
    ):
        raise DomainValidationError("MetricSnapshot requires at least one operational relation")
    await _ensure_exists(session, NewsItem, payload.news_item_id, "News item")
    await _ensure_exists(session, ContentPiece, payload.content_piece_id, "Content piece")
    await _ensure_exists(
        session, DistributionPlan, payload.distribution_plan_id, "Distribution plan"
    )
    await _ensure_exists(
        session, PublicationRecord, payload.publication_record_id, "Publication record"
    )
    await _ensure_exists(session, WorkflowRun, payload.workflow_run_id, "Workflow run")
    await _ensure_exists(session, WorkflowTask, payload.workflow_task_id, "Workflow task")
    await _ensure_exists(session, AgentExecution, payload.agent_execution_id, "Agent execution")
    await _ensure_exists(session, AgentOutput, payload.agent_output_id, "Agent output")


async def _validate_memory_relations(session: AsyncSession, payload: MemoryItemCreate) -> None:
    if payload.entity_type and not payload.entity_id:
        raise DomainValidationError("entity_type and entity_id must be provided together")
    if payload.entity_id and not payload.entity_type:
        raise DomainValidationError("entity_type and entity_id must be provided together")
    if not any(
        [
            payload.entity_type and payload.entity_id,
            payload.news_item_id,
            payload.workflow_run_id,
            payload.agent_output_id,
            payload.audit_check_id,
            payload.metric_snapshot_id,
        ]
    ):
        raise DomainValidationError("MemoryItem requires at least one operational relation")
    await _ensure_exists(session, NewsItem, payload.news_item_id, "News item")
    await _ensure_exists(session, WorkflowRun, payload.workflow_run_id, "Workflow run")
    await _ensure_exists(session, AgentOutput, payload.agent_output_id, "Agent output")
    await _ensure_exists(session, AuditCheck, payload.audit_check_id, "Audit check")
    await _ensure_exists(session, MetricSnapshot, payload.metric_snapshot_id, "Metric snapshot")


async def _validate_knowledge_edge(session: AsyncSession, payload: KnowledgeEdgeCreate) -> None:
    source = await session.get(KnowledgeNode, payload.source_node_id)
    if source is None:
        raise NotFoundError("Source knowledge node")
    target = await session.get(KnowledgeNode, payload.target_node_id)
    if target is None:
        raise NotFoundError("Target knowledge node")
    if payload.relationship_type == "caused_by" and payload.confidence_level in {"KC0", "KC1"}:
        raise ConflictError("caused_by relationships require KC3 or higher confidence")


async def _ensure_exists(session: AsyncSession, model, relation_id: str | None, label: str) -> None:
    if relation_id is None:
        return
    if await session.get(model, relation_id) is None:
        raise NotFoundError(label)
