from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/learning-items", tags=["learning_items"])


@router.post("/", response_model=schemas.LearningItemWithTasks, status_code=status.HTTP_201_CREATED)
def create_learning_item(
    item: schemas.LearningItemCreate,
    db: Session = Depends(get_db)
):
    """
    新規学習項目を作成し、復習タスクを自動生成する
    """
    db_item = crud.create_learning_item(db=db, item=item)
    return db_item


@router.get("/", response_model=schemas.LearningItemListResponse)
def get_learning_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    学習項目の一覧を取得する
    """
    items, total = crud.get_learning_items(db=db, skip=skip, limit=limit)
    return {"items": items, "total": total}


@router.get("/{item_id}", response_model=schemas.LearningItemWithTasks)
def get_learning_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    学習項目の詳細を取得する（復習タスク含む）
    """
    db_item = crud.get_learning_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning item not found"
        )
    return db_item


@router.put("/{item_id}", response_model=schemas.LearningItem)
def update_learning_item(
    item_id: int,
    item_update: schemas.LearningItemUpdate,
    db: Session = Depends(get_db)
):
    """
    学習項目を更新する
    """
    db_item = crud.update_learning_item(db=db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning item not found"
        )
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_learning_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    学習項目を削除する（復習タスクもカスケード削除される）
    """
    success = crud.delete_learning_item(db=db, item_id=item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning item not found"
        )
    return None
