async def test_health(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "xmip-backend",
        "version": "0.1.0",
    }
