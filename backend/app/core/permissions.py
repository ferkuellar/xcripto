from app.core.constants import USER_ROLES

PERMISSIONS = {
    "news.create",
    "news.update_status",
    "source.create",
    "verification.create",
    "risk.create",
    "content.create",
    "content.update_status",
    "audit.create",
    "distribution.create",
    "distribution.update_status",
    "publication.create",
    "publication.update_status",
    "workflow.start",
    "workflow.advance",
    "workflow_task.create",
    "workflow_task.start",
    "workflow_task.complete",
    "workflow_task.fail",
    "workflow_task.block",
    "workflow_task.cancel",
    "workflow_task.retry",
    "agent_output.create",
    "agent_output.accept",
    "agent_output.reject",
    "memory.create",
    "memory.approve",
    "memory.invalidate",
    "knowledge.create",
    "readiness.calculate",
    "intake.create",
    "intake.promote",
    "user.create",
    "user.update",
    "ownership.assign",
    "ownership.release",
}

EDITORIAL_APPROVAL_PERMISSIONS = {
    "news.update_status",
    "audit.create",
    "publication.create",
    "publication.update_status",
    "workflow.start",
    "workflow.advance",
    "content.create",
    "content.update_status",
    "ownership.assign",
    "ownership.release",
    "memory.approve",
    "memory.invalidate",
    "readiness.calculate",
    "intake.promote",
}
EDITOR_PERMISSIONS = {
    "news.create",
    "news.update_status",
    "verification.create",
    "content.create",
    "content.update_status",
    "workflow_task.create",
    "workflow_task.start",
    "workflow_task.complete",
    "workflow_task.fail",
    "workflow_task.block",
    "workflow_task.cancel",
    "workflow_task.retry",
    "intake.create",
    "intake.promote",
}
ANALYST_PERMISSIONS = {
    "verification.create",
    "risk.create",
    "knowledge.create",
    "readiness.calculate",
}
REVIEWER_PERMISSIONS = {
    "verification.create",
    "risk.create",
    "audit.create",
    "memory.create",
    "memory.approve",
    "memory.invalidate",
}
PUBLISHER_PERMISSIONS = {
    "distribution.create",
    "distribution.update_status",
    "publication.create",
    "publication.update_status",
    "workflow_task.create",
    "workflow_task.start",
    "workflow_task.complete",
}
AGENT_OPERATOR_PERMISSIONS = {
    "agent_output.create",
    "agent_output.accept",
    "agent_output.reject",
    "workflow_task.create",
    "workflow_task.start",
    "workflow_task.complete",
    "workflow_task.fail",
    "workflow_task.retry",
}

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "owner": PERMISSIONS,
    "admin": PERMISSIONS,
    "editor_in_chief": EDITORIAL_APPROVAL_PERMISSIONS,
    "editor": EDITOR_PERMISSIONS,
    "analyst": ANALYST_PERMISSIONS,
    "reviewer": REVIEWER_PERMISSIONS,
    "publisher": PUBLISHER_PERMISSIONS,
    "agent_operator": AGENT_OPERATOR_PERMISSIONS,
    "viewer": set(),
    "system": PERMISSIONS,
}


def is_valid_role(role: str) -> bool:
    return role in USER_ROLES


def role_has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())
