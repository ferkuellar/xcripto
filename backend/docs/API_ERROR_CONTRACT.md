# XMIP API Error Contract

The XMIP backend uses standard HTTP status codes and FastAPI-compatible JSON
error responses. Frontend clients should handle `detail` consistently and keep
the current `X-Correlation-ID` available for support/debugging.

## Common Shape

Simple domain/security errors:

```json
{
  "detail": "Missing API key"
}
```

Validation errors:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "display_name"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

Readiness failures:

```json
{
  "status": "not_ready",
  "service": "xmip-backend",
  "version": "0.1.0",
  "checks": {
    "configuration": "ok",
    "database": "failed"
  }
}
```

## Status Codes

### 400 Bad Request

Used for domain validation failures and invalid catalog values.

Examples:

```json
{"detail": "connector_type must be one of ['rss_feed', 'public_api', ...]"}
```

```json
{"detail": "Connector configuration must not contain secrets. Use secret_ref instead."}
```

Frontend behavior: show the message near the form or action that triggered it.

### 401 Unauthorized

Used when `AUTH_ENABLED=true` and the API key header is missing.

```json
{"detail": "Missing API key"}
```

Frontend behavior: show an internal configuration/auth error.

### 403 Forbidden

Used for invalid API key, invalid actor role or insufficient permission.

```json
{"detail": "Invalid API key"}
```

```json
{"detail": "Insufficient permission"}
```

Frontend behavior: show permission denied and current `X-Actor-Role`.

### 404 Not Found

Used when an entity does not exist.

```json
{"detail": "WorkflowTask not found"}
```

Frontend behavior: show a not-found state and offer navigation back to the board.

### 409 Conflict

Used for state conflicts, blocked workflows, retry limit conflicts, editorial
gates and unsafe operations.

Examples:

```json
{"detail": "Workflow is blocked and cannot advance"}
```

```json
{"detail": "Cannot promote duplicate signal"}
```

```json
{"detail": "Connector is archived and cannot run"}
```

Frontend behavior: show a blocking reason and recommended remediation.

### 422 Validation Error

Used by FastAPI/Pydantic when the request shape is invalid.

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "connector_name"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

Frontend behavior: map `loc` to form fields when possible.

### 500 Internal Server Error

Used for unexpected errors or invalid server configuration.

```json
{"detail": "API key auth is enabled but API_KEY is not configured"}
```

Frontend behavior: show generic backend error. In production, do not display
tracebacks or internal stack details.

### 503 Service Unavailable

Used by `/ready` when the backend is not operationally ready.

```json
{
  "status": "not_ready",
  "service": "xmip-backend",
  "checks": {
    "database": "failed"
  }
}
```

Frontend behavior: show maintenance/not-ready state and retry.

## Correlation ID

Frontend clients should generate one `X-Correlation-ID` per user action, for
example:

```text
admin_20260703_153010_abc123
```

Use the same ID across related calls, such as promote signal, start workflow and
calculate readiness. The backend persists this ID on many entities and logs.

## Editorial Gate Errors

Editorial gate errors are usually 400 or 409. They mean the backend refused to
advance state because canonical requirements are missing.

Examples:

- Publication without approved content.
- Published record without URL or external id.
- Content creation blocked by critical risk.
- Workflow advance blocked by missing `VerificationRecord`.

Do not bypass these in the frontend.

