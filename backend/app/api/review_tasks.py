from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/review-tasks", tags=["review_tasks"])


@router.get("/today", response_model=List[schemas.ReviewTask])
def get_today_review_tasks(db: Session = Depends(get_db)):
    """
    今日の復習タスクを取得する
    （due_date が今日以前で未完了のタスク）

    自動的に Pending → Ready の更新も行う
    """
    tasks = crud.get_today_review_tasks(db=db)

    # レスポンスに学習項目の情報を追加
    result = []
    for task in tasks:
        task_dict = schemas.ReviewTask.model_validate(task).model_dump()
        result.append(task_dict)

    return result


@router.get("/{task_id}", response_model=schemas.ReviewTask)
def get_review_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    復習タスクの詳細を取得する
    """
    task = crud.get_review_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review task not found"
        )
    return task


@router.post("/{task_id}/complete", response_model=schemas.ReviewTask)
def complete_review_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    復習タスクを完了する

    1年ごとのタスク（365, 730, 1095, ...日）の場合、
    次の1年後タスクを自動生成する
    """
    try:
        task = crud.complete_review_task(db=db, task_id=task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review task not found"
            )
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{task_id}/uncomplete", response_model=schemas.ReviewTask)
def uncomplete_review_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    復習タスクの完了を取り消す（誤操作対応）
    """
    task = crud.uncomplete_review_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review task not found"
        )
    return task
