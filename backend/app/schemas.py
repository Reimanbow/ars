from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List


# ============================================================================
# Source Schemas
# ============================================================================

class SourceBase(BaseModel):
    """媒体の基本スキーマ"""
    title: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class SourceCreate(SourceBase):
    """媒体作成用スキーマ"""
    pass


class SourceUpdate(BaseModel):
    """媒体更新用スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class Source(SourceBase):
    """媒体レスポンス用スキーマ"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SourceWithItems(Source):
    """学習項目を含む媒体スキーマ"""
    learning_items: List["LearningItem"] = []


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
    source_id: int
    start_date: Optional[date] = None  # 省略時は今日


class LearningItemUpdate(BaseModel):
    """学習項目更新用スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None


class LearningItem(LearningItemBase):
    """学習項目レスポンス用スキーマ"""
    id: int
    source_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LearningItemWithTasks(LearningItem):
    """復習タスク情報を含む学習項目スキーマ"""
    review_tasks: List[ReviewTask] = []


class LearningItemWithSource(LearningItem):
    """媒体情報を含む学習項目スキーマ"""
    source_title: str
    source_category: Optional[str] = None


# ============================================================================
# Response Schemas
# ============================================================================

class SourceListResponse(BaseModel):
    """媒体一覧レスポンス"""
    items: List[Source]
    total: int


class LearningItemListResponse(BaseModel):
    """学習項目一覧レスポンス"""
    items: List[LearningItem]
    total: int


class ErrorResponse(BaseModel):
    """エラーレスポンス"""
    detail: str
