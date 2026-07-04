from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.knowledge import (
    KnowledgeEdgeCreate,
    KnowledgeEdgeRead,
    KnowledgeEntityGraphRead,
    KnowledgeNodeCreate,
    KnowledgeNodeRead,
)
from app.services import metrics_memory_knowledge_service as mmk_service

router = APIRouter(tags=["knowledge"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def _node_to_read(node) -> KnowledgeNodeRead:
    return KnowledgeNodeRead.model_validate(
        {
            "id": node.id,
            "node_type": node.node_type,
            "label": node.label,
            "external_ref": node.external_ref,
            "entity_type": node.entity_type,
            "entity_id": node.entity_id,
            "description": node.description,
            "confidence_level": node.confidence_level,
            "status": node.status,
            "source_or_origin": node.source_or_origin,
            "metadata_json": node.metadata_json,
            "correlation_id": node.correlation_id,
            "created_at": node.created_at,
            "updated_at": node.updated_at,
        }
    )


def _edge_to_read(edge) -> KnowledgeEdgeRead:
    return KnowledgeEdgeRead.model_validate(
        {
            "id": edge.id,
            "source_node_id": edge.source_node_id,
            "target_node_id": edge.target_node_id,
            "relationship_type": edge.relationship_type,
            "scope": edge.scope,
            "confidence_level": edge.confidence_level,
            "reason": edge.reason,
            "status": edge.status,
            "risk_flags": edge.risk_flags,
            "metadata_json": edge.metadata_json,
            "correlation_id": edge.correlation_id,
            "created_at": edge.created_at,
            "updated_at": edge.updated_at,
        }
    )


@router.post(
    "/knowledge/nodes",
    response_model=KnowledgeNodeRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_knowledge_node(
    payload: KnowledgeNodeCreate,
    request: Request,
    session: SessionDep,
) -> KnowledgeNodeRead:
    node = await mmk_service.create_knowledge_node(session, payload, request.state.correlation_id)
    return _node_to_read(node)


@router.get("/knowledge/nodes", response_model=list[KnowledgeNodeRead])
async def list_knowledge_nodes(
    session: SessionDep,
    node_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    confidence_level: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[KnowledgeNodeRead]:
    nodes = await mmk_service.list_knowledge_nodes(
        session,
        node_type=node_type,
        status=status,
        entity_type=entity_type,
        entity_id=entity_id,
        confidence_level=confidence_level,
        limit=limit,
        offset=offset,
    )
    return [_node_to_read(node) for node in nodes]


@router.get("/knowledge/nodes/{node_id}", response_model=KnowledgeNodeRead)
async def get_knowledge_node(node_id: str, session: SessionDep) -> KnowledgeNodeRead:
    node = await mmk_service.get_knowledge_node(session, node_id)
    return _node_to_read(node)


@router.post(
    "/knowledge/edges",
    response_model=KnowledgeEdgeRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_knowledge_edge(
    payload: KnowledgeEdgeCreate,
    request: Request,
    session: SessionDep,
) -> KnowledgeEdgeRead:
    edge = await mmk_service.create_knowledge_edge(session, payload, request.state.correlation_id)
    return _edge_to_read(edge)


@router.get("/knowledge/edges", response_model=list[KnowledgeEdgeRead])
async def list_knowledge_edges(
    session: SessionDep,
    source_node_id: str | None = Query(default=None),
    target_node_id: str | None = Query(default=None),
    relationship_type: str | None = Query(default=None),
    scope: str | None = Query(default=None),
    status: str | None = Query(default=None),
    confidence_level: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[KnowledgeEdgeRead]:
    edges = await mmk_service.list_knowledge_edges(
        session,
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        relationship_type=relationship_type,
        scope=scope,
        status=status,
        confidence_level=confidence_level,
        limit=limit,
        offset=offset,
    )
    return [_edge_to_read(edge) for edge in edges]


@router.get("/knowledge/edges/{edge_id}", response_model=KnowledgeEdgeRead)
async def get_knowledge_edge(edge_id: str, session: SessionDep) -> KnowledgeEdgeRead:
    edge = await mmk_service.get_knowledge_edge(session, edge_id)
    return _edge_to_read(edge)


@router.get("/knowledge/nodes/{node_id}/edges", response_model=list[KnowledgeEdgeRead])
async def list_node_edges(
    node_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[KnowledgeEdgeRead]:
    edges = await mmk_service.list_knowledge_edges_for_node(
        session, node_id, limit=limit, offset=offset
    )
    return [_edge_to_read(edge) for edge in edges]


@router.get("/knowledge/entity/{entity_type}/{entity_id}", response_model=KnowledgeEntityGraphRead)
async def get_knowledge_entity(
    entity_type: str,
    entity_id: str,
    session: SessionDep,
) -> KnowledgeEntityGraphRead:
    graph = await mmk_service.get_knowledge_entity_graph(session, entity_type, entity_id)
    return KnowledgeEntityGraphRead(
        nodes=[_node_to_read(node) for node in graph["nodes"]],
        edges=[_edge_to_read(edge) for edge in graph["edges"]],
    )
