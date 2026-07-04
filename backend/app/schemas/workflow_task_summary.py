from pydantic import BaseModel


class WorkflowTaskSummary(BaseModel):
    task_count: int
    pending_task_count: int
    blocking_task_count: int
    completed_task_count: int
