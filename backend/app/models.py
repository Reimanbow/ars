from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class LearningItem(Base):
    """学習項目モデル"""
    __tablename__ = "learning_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship with ReviewTask
    review_tasks = relationship(
        "ReviewTask",
        back_populates="learning_item",
        cascade="all, delete-orphan"
    )


class ReviewTask(Base):
    """復習タスクモデル"""
    __tablename__ = "review_tasks"

    id = Column(Integer, primary_key=True, index=True)
    learning_item_id = Column(Integer, ForeignKey("learning_items.id", ondelete="CASCADE"), nullable=False)
    stage_name = Column(String(50), nullable=False)
    stage_offset_days = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String(20), default="Pending", nullable=False)  # Pending, Ready, Completed
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship with LearningItem
    learning_item = relationship("LearningItem", back_populates="review_tasks")

    # Indexes for performance
    __table_args__ = (
        Index('idx_learning_item_id', 'learning_item_id'),
        Index('idx_due_date', 'due_date'),
        Index('idx_status', 'status'),
    )
