from sqlalchemy.orm import Session, joinedload
from datetime import date, datetime, timedelta
from typing import List, Optional
from app import models, schemas
from app.scheduler import generate_review_tasks, generate_next_yearly_task


# ============================================================================
# Source CRUD Operations
# ============================================================================

def create_source(db: Session, source: schemas.SourceCreate) -> models.Source:
    """
    新規媒体を作成する

    Args:
        db: データベースセッション
        source: 媒体作成スキーマ

    Returns:
        作成された媒体
    """
    db_source = models.Source(
        title=source.title,
        category=source.category,
        description=source.description
    )
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def get_sources(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> tuple[List[models.Source], int]:
    """
    媒体の一覧を取得する

    Args:
        db: データベースセッション
        skip: スキップする件数
        limit: 取得する最大件数

    Returns:
        (媒体のリスト, 総件数) のタプル
    """
    total = db.query(models.Source).count()
    sources = db.query(models.Source)\
        .order_by(models.Source.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return sources, total


def get_source(db: Session, source_id: int) -> Optional[models.Source]:
    """
    媒体の詳細を取得する（学習項目含む）

    Args:
        db: データベースセッション
        source_id: 媒体ID

    Returns:
        媒体（見つからない場合はNone）
    """
    return db.query(models.Source)\
        .options(joinedload(models.Source.learning_items))\
        .filter(models.Source.id == source_id)\
        .first()


def update_source(
    db: Session,
    source_id: int,
    source_update: schemas.SourceUpdate
) -> Optional[models.Source]:
    """
    媒体を更新する

    Args:
        db: データベースセッション
        source_id: 媒体ID
        source_update: 更新内容

    Returns:
        更新された媒体（見つからない場合はNone）
    """
    db_source = db.query(models.Source).filter(models.Source.id == source_id).first()
    if not db_source:
        return None

    update_data = source_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_source, key, value)

    db.commit()
    db.refresh(db_source)
    return db_source


def delete_source(db: Session, source_id: int) -> bool:
    """
    媒体を削除する（学習項目・復習タスクもカスケード削除される）

    Args:
        db: データベースセッション
        source_id: 媒体ID

    Returns:
        削除成功ならTrue、見つからない場合はFalse
    """
    db_source = db.query(models.Source).filter(models.Source.id == source_id).first()
    if not db_source:
        return False

    db.delete(db_source)
    db.commit()
    return True


# ============================================================================
# Learning Item CRUD Operations
# ============================================================================

def create_learning_item(
    db: Session,
    item: schemas.LearningItemCreate
) -> models.LearningItem:
    """
    新規学習項目を作成し、復習タスクを自動生成する

    Args:
        db: データベースセッション
        item: 学習項目作成スキーマ

    Returns:
        作成された学習項目（復習タスク含む）
    """
    # 学習項目を作成
    db_item = models.LearningItem(
        source_id=item.source_id,
        title=item.title,
        content=item.content
    )
    db.add(db_item)
    db.flush()  # IDを取得するためにflush

    # 開始日を取得（省略時は今日）
    start_date = item.start_date if item.start_date else date.today()

    # 復習タスクを生成
    tasks_data = generate_review_tasks(db_item.id, start_date)
    for task_data in tasks_data:
        db_task = models.ReviewTask(**task_data)
        db.add(db_task)

    db.commit()
    db.refresh(db_item)
    return db_item


def get_learning_items(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> tuple[List[models.LearningItem], int]:
    """
    学習項目の一覧を取得する

    Args:
        db: データベースセッション
        skip: スキップする件数
        limit: 取得する最大件数

    Returns:
        (学習項目のリスト, 総件数) のタプル
    """
    total = db.query(models.LearningItem).count()
    items = db.query(models.LearningItem)\
        .order_by(models.LearningItem.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return items, total


def get_learning_item(db: Session, item_id: int) -> Optional[models.LearningItem]:
    """
    学習項目の詳細を取得する（復習タスク含む）

    Args:
        db: データベースセッション
        item_id: 学習項目ID

    Returns:
        学習項目（見つからない場合はNone）
    """
    return db.query(models.LearningItem)\
        .options(joinedload(models.LearningItem.review_tasks))\
        .filter(models.LearningItem.id == item_id)\
        .first()


def update_learning_item(
    db: Session,
    item_id: int,
    item_update: schemas.LearningItemUpdate
) -> Optional[models.LearningItem]:
    """
    学習項目を更新する

    Args:
        db: データベースセッション
        item_id: 学習項目ID
        item_update: 更新内容

    Returns:
        更新された学習項目（見つからない場合はNone）
    """
    db_item = db.query(models.LearningItem).filter(models.LearningItem.id == item_id).first()
    if not db_item:
        return None

    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_learning_item(db: Session, item_id: int) -> bool:
    """
    学習項目を削除する（復習タスクもカスケード削除される）

    Args:
        db: データベースセッション
        item_id: 学習項目ID

    Returns:
        削除成功ならTrue、見つからない場合はFalse
    """
    db_item = db.query(models.LearningItem).filter(models.LearningItem.id == item_id).first()
    if not db_item:
        return False

    db.delete(db_item)
    db.commit()
    return True


# ============================================================================
# Review Task CRUD Operations
# ============================================================================

def get_today_review_tasks(db: Session) -> List[models.ReviewTask]:
    """
    今日の復習タスクを取得する
    （due_date が今日以前で未完了のタスク）

    同時に Pending → Ready の自動更新も行う

    Args:
        db: データベースセッション

    Returns:
        今日の復習タスクのリスト
    """
    today = date.today()

    # Pending → Ready の自動更新
    db.query(models.ReviewTask)\
        .filter(
            models.ReviewTask.due_date <= today,
            models.ReviewTask.status == "Pending"
        )\
        .update({"status": "Ready"})
    db.commit()

    # Ready状態のタスクを取得（学習項目も一緒にロード）
    tasks = db.query(models.ReviewTask)\
        .options(joinedload(models.ReviewTask.learning_item))\
        .filter(models.ReviewTask.status == "Ready")\
        .order_by(models.ReviewTask.due_date)\
        .all()

    return tasks


def get_review_task(db: Session, task_id: int) -> Optional[models.ReviewTask]:
    """
    復習タスクの詳細を取得する

    Args:
        db: データベースセッション
        task_id: 復習タスクID

    Returns:
        復習タスク（見つからない場合はNone）
    """
    return db.query(models.ReviewTask)\
        .filter(models.ReviewTask.id == task_id)\
        .first()


def complete_review_task(db: Session, task_id: int) -> Optional[models.ReviewTask]:
    """
    復習タスクを完了する

    1年ごとのタスク（365, 730, 1095, ...日）の場合、
    次の1年後タスクを自動生成する

    Args:
        db: データベースセッション
        task_id: 復習タスクID

    Returns:
        完了した復習タスク（見つからない場合はNone）

    Raises:
        ValueError: 既に完了済みの場合
    """
    task = db.query(models.ReviewTask).filter(models.ReviewTask.id == task_id).first()
    if not task:
        return None

    if task.status == "Completed":
        raise ValueError("Task is already completed")

    # 完了処理
    task.status = "Completed"
    task.completed_at = datetime.utcnow()
    db.commit()

    # 1年ごとのタスクの場合、次のタスクを生成
    if task.stage_offset_days >= 365 and task.stage_offset_days % 365 == 0:
        next_task_data = generate_next_yearly_task(
            task.learning_item_id,
            task.stage_offset_days,
            task.due_date
        )
        next_task = models.ReviewTask(**next_task_data)
        db.add(next_task)
        db.commit()

    db.refresh(task)
    return task


def uncomplete_review_task(db: Session, task_id: int) -> Optional[models.ReviewTask]:
    """
    復習タスクの完了を取り消す（誤操作対応）

    Args:
        db: データベースセッション
        task_id: 復習タスクID

    Returns:
        取り消された復習タスク（見つからない場合はNone）
    """
    task = db.query(models.ReviewTask).filter(models.ReviewTask.id == task_id).first()
    if not task:
        return None

    task.status = "Ready"
    task.completed_at = None
    db.commit()
    db.refresh(task)
    return task
