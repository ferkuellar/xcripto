from app.core.config import get_settings
from tests.test_editorial_core import (
    create_news_item,
    create_publishable_chain,
    publication_record_payload,
)
from tests.test_workflows import start_workflow


def metric_snapshot_payload(news_id: str, **overrides) -> dict:
    payload = {
        "news_item_id": news_id,
        "metric_category": "publication_metrics",
        "measurement_window": "24h",
        "metric_name": "views",
        "metric_value": 1200.0,
        "snapshot_payload": {"views": 1200, "likes": 45},
        "source_or_origin": "manual editorial capture",
        "data_quality": "high",
    }
    return {**payload, **overrides}


def memory_item_payload(news_id: str, **overrides) -> dict:
    payload = {
        "memory_type": "editorial_memory",
        "title": "Source double-check rule",
        "memory_statement": "Critical editorial claims require a second source.",
        "why_it_matters": "Prevents single-source amplification.",
        "how_to_use": "Apply to market-sensitive items.",
        "how_not_to_use": "Do not treat as factual verification.",
        "source_or_origin": "Editorial review after publication",
        "news_item_id": news_id,
        "confidence_level": "MC3",
        "persistence_level": "M2",
        "scope": "project_wide",
        "risk_flags": ["verification_gap"],
        "expiration_recommendation": "review_quarterly",
    }
    return {**payload, **overrides}


def knowledge_node_payload(label: str, **overrides) -> dict:
    payload = {
        "node_type": "ContentPiece",
        "label": label,
        "entity_type": "content_piece",
        "entity_id": "content-piece-id",
        "description": "Editorial node.",
        "confidence_level": "KC3",
        "status": "approved",
        "source_or_origin": "Editorial system",
        "metadata": {"kind": "editorial"},
    }
    return {**payload, **overrides}


def knowledge_edge_payload(source_node_id: str, target_node_id: str, **overrides) -> dict:
    payload = {
        "source_node_id": source_node_id,
        "target_node_id": target_node_id,
        "relationship_type": "derived_memory_from",
        "scope": "memory_context",
        "confidence_level": "KC3",
        "reason": "Memory derived from the editorial artifact.",
        "status": "approved",
        "risk_flags": [],
        "metadata": {"kind": "trace"},
    }
    return {**payload, **overrides}


async def create_metric_snapshot(client, news_id: str, **overrides) -> dict:
    response = await client.post(
        "/api/v1/metric-snapshots",
        json=metric_snapshot_payload(news_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


async def create_memory_item(client, news_id: str, **overrides) -> dict:
    response = await client.post(
        "/api/v1/memory-items",
        json=memory_item_payload(news_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


async def create_knowledge_node(client, label: str, **overrides) -> dict:
    response = await client.post(
        "/api/v1/knowledge/nodes",
        json=knowledge_node_payload(label, **overrides),
    )
    assert response.status_code == 201
    return response.json()


async def create_knowledge_edge(
    client, source_node_id: str, target_node_id: str, **overrides
) -> dict:
    response = await client.post(
        "/api/v1/knowledge/edges",
        json=knowledge_edge_payload(source_node_id, target_node_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


async def test_create_metric_snapshot_valid(client):
    news = await create_news_item(client)

    snapshot = await create_metric_snapshot(client, news["id"])

    assert snapshot["news_item_id"] == news["id"]
    assert snapshot["metric_name"] == "views"


async def test_create_metric_snapshot_blocks_missing_relation(client):
    response = await client.post(
        "/api/v1/metric-snapshots",
        json={
            "metric_category": "publication_metrics",
            "measurement_window": "24h",
            "metric_name": "views",
            "metric_value": 1.0,
            "source_or_origin": "manual capture",
            "data_quality": "high",
        },
    )

    assert response.status_code == 400


async def test_create_metric_snapshot_blocks_invalid_category(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/metric-snapshots",
        json=metric_snapshot_payload(news["id"], metric_category="not-a-category"),
    )

    assert response.status_code == 422


async def test_create_metric_snapshot_blocks_invalid_measurement_window(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/metric-snapshots",
        json=metric_snapshot_payload(news["id"], measurement_window="2h"),
    )

    assert response.status_code == 422


async def test_create_metric_snapshot_blocks_invalid_data_quality(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/metric-snapshots",
        json=metric_snapshot_payload(news["id"], data_quality="garbage"),
    )

    assert response.status_code == 422


async def test_list_metric_snapshots(client):
    news = await create_news_item(client)
    await create_metric_snapshot(client, news["id"])

    response = await client.get("/api/v1/metric-snapshots")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_metric_snapshots_by_news_item(client):
    news = await create_news_item(client)
    await create_metric_snapshot(client, news["id"])

    response = await client.get("/api/v1/metric-snapshots", params={"news_item_id": news["id"]})

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_metric_snapshots_by_workflow_run_id(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_metric_snapshot(client, news["id"], workflow_run_id=workflow["id"])

    response = await client.get(
        "/api/v1/metric-snapshots",
        params={"workflow_run_id": workflow["id"]},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_metric_snapshot_by_id(client):
    news = await create_news_item(client)
    snapshot = await create_metric_snapshot(client, news["id"])

    response = await client.get(f"/api/v1/metric-snapshots/{snapshot['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == snapshot["id"]


async def test_get_metric_snapshots_by_news_id(client):
    news = await create_news_item(client)
    await create_metric_snapshot(client, news["id"])

    response = await client.get(f"/api/v1/news/{news['id']}/metric-snapshots")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_metric_snapshots_by_publication_record_id(client):
    news, piece, plan = await create_publishable_chain(client)
    publication = await client.post(
        "/api/v1/publication-records",
        json=publication_record_payload(news["id"], piece["id"], plan["id"]),
    )
    assert publication.status_code == 201
    publication_id = publication.json()["id"]
    await create_metric_snapshot(client, news["id"], publication_record_id=publication_id)

    response = await client.get(
        f"/api/v1/publication-records/{publication_id}/metric-snapshots"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_metric_snapshots_by_workflow_run_id(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_metric_snapshot(client, news["id"], workflow_run_id=workflow["id"])

    response = await client.get(f"/api/v1/workflows/{workflow['id']}/metric-snapshots")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_metric_snapshot_correlation_id_persisted(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/metric-snapshots",
        json=metric_snapshot_payload(news["id"]),
        headers={"X-Correlation-ID": "corr-metric-001"},
    )

    assert response.status_code == 201
    assert response.json()["correlation_id"] == "corr-metric-001"


async def test_auth_protects_metric_snapshot_post(client, monkeypatch):
    news = await create_news_item(client)
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(
        "/api/v1/metric-snapshots",
        json=metric_snapshot_payload(news["id"]),
    )

    assert response.status_code == 401


async def test_create_memory_item_valid(client):
    news = await create_news_item(client)

    memory = await create_memory_item(client, news["id"])

    assert memory["news_item_id"] == news["id"]
    assert memory["memory_status"] == "proposed"


async def test_create_memory_item_blocks_missing_relation(client):
    response = await client.post(
        "/api/v1/memory-items",
        json={
            "memory_type": "editorial_memory",
            "title": "Orphan memory",
            "memory_statement": "No relation.",
            "source_or_origin": "manual",
            "confidence_level": "MC2",
            "persistence_level": "M2",
            "scope": "project_wide",
            "expiration_recommendation": "review_quarterly",
        },
    )

    assert response.status_code == 400


async def test_create_memory_item_blocks_invalid_type(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/memory-items",
        json=memory_item_payload(news["id"], memory_type="not-a-type"),
    )

    assert response.status_code == 422


async def test_create_memory_item_blocks_missing_origin(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/memory-items",
        json=memory_item_payload(news["id"], source_or_origin=""),
    )

    assert response.status_code == 422


async def test_memory_item_auto_human_review_for_sensitive_types(client):
    news = await create_news_item(client)

    memory = await create_memory_item(client, news["id"], memory_type="source_memory")

    assert memory["human_review_required"] is True


async def test_approve_memory_item(client):
    news = await create_news_item(client)
    memory = await create_memory_item(client, news["id"])

    response = await client.patch(
        f"/api/v1/memory-items/{memory['id']}/approve",
        json={"approved_by": "operator"},
    )

    assert response.status_code == 200
    assert response.json()["memory_status"] == "approved"
    assert response.json()["approved_by"] == "operator"


async def test_reject_memory_item(client):
    news = await create_news_item(client)
    memory = await create_memory_item(client, news["id"])

    response = await client.patch(
        f"/api/v1/memory-items/{memory['id']}/reject",
        json={"reason": "Insufficient origin."},
    )

    assert response.status_code == 200
    assert response.json()["memory_status"] == "rejected"


async def test_invalidate_memory_item(client):
    news = await create_news_item(client)
    memory = await create_memory_item(client, news["id"])

    response = await client.patch(
        f"/api/v1/memory-items/{memory['id']}/invalidate",
        json={"invalidated_by": "operator", "reason": "Context changed."},
    )

    assert response.status_code == 200
    assert response.json()["memory_status"] == "invalidated"


async def test_archive_memory_item(client):
    news = await create_news_item(client)
    memory = await create_memory_item(client, news["id"])

    response = await client.patch(
        f"/api/v1/memory-items/{memory['id']}/archive",
        json={"reason": "Archived after review."},
    )

    assert response.status_code == 200
    assert response.json()["memory_status"] == "archived"


async def test_memory_item_blocks_approve_after_invalidation(client):
    news = await create_news_item(client)
    memory = await create_memory_item(client, news["id"])
    invalidated = await client.patch(
        f"/api/v1/memory-items/{memory['id']}/invalidate",
        json={"invalidated_by": "operator", "reason": "Context changed."},
    )
    assert invalidated.status_code == 200

    response = await client.patch(
        f"/api/v1/memory-items/{memory['id']}/approve",
        json={"approved_by": "operator"},
    )

    assert response.status_code == 409


async def test_list_memory_items(client):
    news = await create_news_item(client)
    await create_memory_item(client, news["id"])

    response = await client.get("/api/v1/memory-items")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_memory_items_by_type(client):
    news = await create_news_item(client)
    await create_memory_item(client, news["id"])

    response = await client.get("/api/v1/memory-items", params={"memory_type": "editorial_memory"})

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_memory_items_by_status(client):
    news = await create_news_item(client)
    await create_memory_item(client, news["id"])

    response = await client.get("/api/v1/memory-items", params={"memory_status": "proposed"})

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_memory_item_by_id(client):
    news = await create_news_item(client)
    memory = await create_memory_item(client, news["id"])

    response = await client.get(f"/api/v1/memory-items/{memory['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == memory["id"]


async def test_get_memory_items_by_news_id(client):
    news = await create_news_item(client)
    await create_memory_item(client, news["id"])

    response = await client.get(f"/api/v1/news/{news['id']}/memory-items")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_memory_items_by_workflow_run_id(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_memory_item(client, news["id"], workflow_run_id=workflow["id"])

    response = await client.get(f"/api/v1/workflows/{workflow['id']}/memory-items")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_auth_protects_memory_item_post(client, monkeypatch):
    news = await create_news_item(client)
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post("/api/v1/memory-items", json=memory_item_payload(news["id"]))

    assert response.status_code == 401


async def test_auth_protects_memory_item_patch(client, monkeypatch):
    news = await create_news_item(client)
    memory = await create_memory_item(client, news["id"])
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.patch(
        f"/api/v1/memory-items/{memory['id']}/approve",
        json={"approved_by": "operator"},
    )

    assert response.status_code == 401


async def test_create_knowledge_node_valid(client):
    node = await create_knowledge_node(client, "Editorial content node")

    assert node["label"] == "Editorial content node"
    assert node["node_type"] == "ContentPiece"


async def test_create_knowledge_node_blocks_missing_label(client):
    response = await client.post(
        "/api/v1/knowledge/nodes",
        json={
            "node_type": "ContentPiece",
            "label": "",
            "entity_type": "content_piece",
            "entity_id": "content-piece-id",
            "description": "Editorial node.",
            "confidence_level": "KC3",
            "status": "approved",
            "source_or_origin": "Editorial system",
            "metadata": {"kind": "editorial"},
        },
    )

    assert response.status_code == 422


async def test_create_knowledge_node_blocks_missing_origin(client):
    response = await client.post(
        "/api/v1/knowledge/nodes",
        json=knowledge_node_payload("Node", source_or_origin=""),
    )

    assert response.status_code == 422


async def test_create_knowledge_node_blocks_invalid_type(client):
    response = await client.post(
        "/api/v1/knowledge/nodes",
        json=knowledge_node_payload("Node", node_type="NotReal"),
    )

    assert response.status_code == 422


async def test_list_knowledge_nodes(client):
    await create_knowledge_node(client, "Editorial content node")

    response = await client.get("/api/v1/knowledge/nodes")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_knowledge_nodes_by_entity(client):
    await create_knowledge_node(
        client,
        "Editorial content node",
        entity_type="content_piece",
        entity_id="piece-1",
    )

    response = await client.get(
        "/api/v1/knowledge/nodes",
        params={"entity_type": "content_piece", "entity_id": "piece-1"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_knowledge_node_by_id(client):
    node = await create_knowledge_node(client, "Editorial content node")

    response = await client.get(f"/api/v1/knowledge/nodes/{node['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == node["id"]


async def test_create_knowledge_edge_valid(client):
    source = await create_knowledge_node(client, "Source node")
    target = await create_knowledge_node(client, "Memory node", node_type="MemoryItem")

    edge = await create_knowledge_edge(client, source["id"], target["id"])

    assert edge["source_node_id"] == source["id"]
    assert edge["target_node_id"] == target["id"]


async def test_create_knowledge_edge_blocks_self_reference(client):
    node = await create_knowledge_node(client, "Loop node")

    response = await client.post(
        "/api/v1/knowledge/edges",
        json=knowledge_edge_payload(node["id"], node["id"]),
    )

    assert response.status_code == 422


async def test_create_knowledge_edge_blocks_missing_source_node(client):
    target = await create_knowledge_node(client, "Target node")

    response = await client.post(
        "/api/v1/knowledge/edges",
        json=knowledge_edge_payload("missing-source", target["id"]),
    )

    assert response.status_code == 404


async def test_create_knowledge_edge_blocks_invalid_relationship(client):
    source = await create_knowledge_node(client, "Source node")
    target = await create_knowledge_node(client, "Target node")

    response = await client.post(
        "/api/v1/knowledge/edges",
        json=knowledge_edge_payload(source["id"], target["id"], relationship_type="not-real"),
    )

    assert response.status_code == 422


async def test_create_knowledge_edge_blocks_low_confidence_causality(client):
    source = await create_knowledge_node(client, "Source node")
    target = await create_knowledge_node(client, "Target node")

    response = await client.post(
        "/api/v1/knowledge/edges",
        json=knowledge_edge_payload(
            source["id"],
            target["id"],
            relationship_type="caused_by",
            confidence_level="KC1",
        ),
    )

    assert response.status_code == 409


async def test_list_knowledge_edges(client):
    source = await create_knowledge_node(client, "Source node")
    target = await create_knowledge_node(client, "Target node")
    await create_knowledge_edge(client, source["id"], target["id"])

    response = await client.get("/api/v1/knowledge/edges")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_edges_for_node(client):
    source = await create_knowledge_node(client, "Source node")
    target = await create_knowledge_node(client, "Target node")
    await create_knowledge_edge(client, source["id"], target["id"])

    response = await client.get(f"/api/v1/knowledge/nodes/{source['id']}/edges")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_knowledge_entity_graph(client):
    node = await create_knowledge_node(
        client,
        "Editorial content node",
        entity_type="content_piece",
        entity_id="piece-graph-1",
    )

    response = await client.get("/api/v1/knowledge/entity/content_piece/piece-graph-1")

    assert response.status_code == 200
    assert response.json()["nodes"][0]["id"] == node["id"]


async def test_auth_protects_knowledge_node_post(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post("/api/v1/knowledge/nodes", json=knowledge_node_payload("Node"))

    assert response.status_code == 401


async def test_auth_protects_knowledge_edge_post(client, monkeypatch):
    source = await create_knowledge_node(client, "Source node")
    target = await create_knowledge_node(client, "Target node")
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(
        "/api/v1/knowledge/edges",
        json=knowledge_edge_payload(source["id"], target["id"]),
    )

    assert response.status_code == 401
