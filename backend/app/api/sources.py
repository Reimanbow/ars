from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("/", response_model=schemas.Source, status_code=status.HTTP_201_CREATED)
def create_source(
    source: schemas.SourceCreate,
    db: Session = Depends(get_db)
):
    """
    新規媒体（書籍・教材など）を作成する
    """
    db_source = crud.create_source(db=db, source=source)
    return db_source


@router.get("/", response_model=schemas.SourceListResponse)
def get_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    媒体の一覧を取得する
    """
    sources, total = crud.get_sources(db=db, skip=skip, limit=limit)
    return {"items": sources, "total": total}


@router.get("/{source_id}", response_model=schemas.SourceWithItems)
def get_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    """
    媒体の詳細を取得する（学習項目含む）
    """
    db_source = crud.get_source(db=db, source_id=source_id)
    if db_source is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )
    return db_source


@router.put("/{source_id}", response_model=schemas.Source)
def update_source(
    source_id: int,
    source_update: schemas.SourceUpdate,
    db: Session = Depends(get_db)
):
    """
    媒体を更新する
    """
    db_source = crud.update_source(db=db, source_id=source_id, source_update=source_update)
    if db_source is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )
    return db_source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    """
    媒体を削除する（学習項目・復習タスクもカスケード削除される）
    """
    success = crud.delete_source(db=db, source_id=source_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )
    return None
