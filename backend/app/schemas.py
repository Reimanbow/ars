from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List


# ============================================================================
# Review Task Schemas
# ============================================================================

class ReviewTaskBase(BaseModel):
    """復習タスクの基本スキーマ"""
    stage_name: str
    stage_offset_days: int
    due_date: date
    status: str = "Pending"


class ReviewTaskCreate(ReviewTaskBase):
    """復習タスク作成用スキーマ"""
    learning_item_id: int


class ReviewTask(ReviewTaskBase):
    """復習タスクレスポンス用スキーマ"""
    id: int
    learning_item_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewTaskWithItem(ReviewTask):
    """学習項目情報を含む復習タスクスキーマ"""
    learning_item_title: str
    learning_item_content: Optional[str] = None


# ============================================================================
# Learning Item Schemas
# ============================================================================

class LearningItemBase(BaseModel):
    """学習項目の基本スキーマ"""
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None


class LearningItemCreate(LearningItemBase):
    """学習項目作成用スキーマ"""
    start_date: Optional[date] = None  # 省略時は今日


class LearningItemUpdate(BaseModel):
    """学習項目更新用スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None


class LearningItem(LearningItemBase):
    """学習項目レスポンス用スキーマ"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LearningItemWithTasks(LearningItem):
    """復習タスク情報を含む学習項目スキーマ"""
    review_tasks: List[ReviewTask] = []


# ============================================================================
# Response Schemas
# ============================================================================

class LearningItemListResponse(BaseModel):
    """学習項目一覧レスポンス"""
    items: List[LearningItem]
    total: int


class ErrorResponse(BaseModel):
    """エラーレスポンス"""
    detail: str
