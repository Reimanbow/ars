from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import learning_items, review_tasks

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

# FastAPIアプリケーションを作成
app = FastAPI(
    title="Active Recall Scheduler API",
    description="忘却曲線に基づく復習スケジューラーAPI",
    version="1.0.0"
)

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録
app.include_router(learning_items.router, prefix="/api")
app.include_router(review_tasks.router, prefix="/api")


@app.get("/")
def root():
    """ルートエンドポイント"""
    return {
        "message": "Active Recall Scheduler API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}
