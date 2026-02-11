from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..dependencies import get_session, verify_jwt
from ..models.task import Task
from ..schemas.responses import DeleteResponse, SuccessResponse
from ..schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter()


def _verify_user_id(user_id: UUID, token_payload: dict) -> None:
    if str(user_id) != token_payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch",
        )


def _get_task_or_404(
    session: Session, task_id: UUID, user_id: UUID
) -> Task:
    statement = select(Task).where(
        Task.id == task_id, Task.user_id == user_id
    )
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


# ── US1: Create and List Tasks ──


@router.post(
    "/{user_id}/tasks",
    response_model=SuccessResponse[TaskRead],
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    token_payload: dict = Depends(verify_jwt),
):
    _verify_user_id(user_id, token_payload)
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return SuccessResponse(
        data=TaskRead.model_validate(task),
        message="Task created successfully",
    )


@router.get(
    "/{user_id}/tasks",
    response_model=SuccessResponse[list[TaskRead]],
)
def list_tasks(
    user_id: UUID,
    session: Session = Depends(get_session),
    token_payload: dict = Depends(verify_jwt),
):
    _verify_user_id(user_id, token_payload)
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return SuccessResponse(
        data=[TaskRead.model_validate(t) for t in tasks],
    )


# ── US2: View, Update, Delete ──


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=SuccessResponse[TaskRead],
)
def get_task(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session),
    token_payload: dict = Depends(verify_jwt),
):
    _verify_user_id(user_id, token_payload)
    task = _get_task_or_404(session, task_id, user_id)
    return SuccessResponse(data=TaskRead.model_validate(task))


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=SuccessResponse[TaskRead],
)
def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    token_payload: dict = Depends(verify_jwt),
):
    _verify_user_id(user_id, token_payload)
    task = _get_task_or_404(session, task_id, user_id)
    task.title = task_data.title
    task.description = task_data.description
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return SuccessResponse(
        data=TaskRead.model_validate(task),
        message="Task updated successfully",
    )


@router.delete(
    "/{user_id}/tasks/{task_id}",
    response_model=DeleteResponse,
)
def delete_task(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session),
    token_payload: dict = Depends(verify_jwt),
):
    _verify_user_id(user_id, token_payload)
    task = _get_task_or_404(session, task_id, user_id)
    session.delete(task)
    session.commit()
    return DeleteResponse(message="Task deleted successfully")


# ── US3: Mark Task as Complete ──


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=SuccessResponse[TaskRead],
)
def complete_task(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session),
    token_payload: dict = Depends(verify_jwt),
):
    _verify_user_id(user_id, token_payload)
    task = _get_task_or_404(session, task_id, user_id)
    if not task.is_completed:
        task.is_completed = True
        task.completed_at = datetime.now(timezone.utc)
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
    return SuccessResponse(
        data=TaskRead.model_validate(task),
        message="Task marked as complete",
    )
