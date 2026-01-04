import pytest
from fastapi.testclient import TestClient
from datetime import date
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Active Recall Scheduler API"
    assert "version" in data


def test_health_check():
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_learning_item():
    """学習項目作成のテスト"""
    response = client.post(
        "/api/learning-items/",
        json={
            "title": "Test Item",
            "content": "Test content"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["content"] == "Test content"
    assert "id" in data
    assert "review_tasks" in data
    assert len(data["review_tasks"]) == 9  # 9個の復習タスクが生成される


def test_create_learning_item_with_start_date():
    """開始日指定での学習項目作成のテスト"""
    response = client.post(
        "/api/learning-items/",
        json={
            "title": "Test Item with Date",
            "content": "Test content",
            "start_date": "2024-01-01"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Item with Date"

    # 最初のタスクの予定日が2024-01-01であることを確認
    review_tasks = sorted(data["review_tasks"], key=lambda x: x["stage_offset_days"])
    assert review_tasks[0]["due_date"] == "2024-01-01"


def test_get_learning_items():
    """学習項目一覧取得のテスト"""
    response = client.get("/api/learning-items/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


def test_get_learning_item_detail():
    """学習項目詳細取得のテスト"""
    # まず学習項目を作成
    create_response = client.post(
        "/api/learning-items/",
        json={"title": "Test Item for Detail", "content": "Detail content"}
    )
    item_id = create_response.json()["id"]

    # 詳細を取得
    response = client.get(f"/api/learning-items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == "Test Item for Detail"
    assert "review_tasks" in data


def test_get_nonexistent_learning_item():
    """存在しない学習項目の取得テスト"""
    response = client.get("/api/learning-items/9999")
    assert response.status_code == 404


def test_update_learning_item():
    """学習項目更新のテスト"""
    # まず学習項目を作成
    create_response = client.post(
        "/api/learning-items/",
        json={"title": "Original Title", "content": "Original content"}
    )
    item_id = create_response.json()["id"]

    # 更新
    response = client.put(
        f"/api/learning-items/{item_id}",
        json={"title": "Updated Title", "content": "Updated content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"


def test_delete_learning_item():
    """学習項目削除のテスト"""
    # まず学習項目を作成
    create_response = client.post(
        "/api/learning-items/",
        json={"title": "Item to Delete"}
    )
    item_id = create_response.json()["id"]

    # 削除
    response = client.delete(f"/api/learning-items/{item_id}")
    assert response.status_code == 204

    # 削除後に取得を試みる
    get_response = client.get(f"/api/learning-items/{item_id}")
    assert get_response.status_code == 404


def test_get_today_reviews():
    """今日の復習タスク取得のテスト"""
    response = client.get("/api/review-tasks/today")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_complete_review_task():
    """復習タスク完了のテスト"""
    # 学習項目を作成
    create_response = client.post(
        "/api/learning-items/",
        json={"title": "Item for Review"}
    )
    review_tasks = create_response.json()["review_tasks"]

    # 最初のタスク（学習直後）を完了
    task_id = review_tasks[0]["id"]
    response = client.post(f"/api/review-tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Completed"
    assert data["completed_at"] is not None


def test_complete_already_completed_task():
    """既に完了済みのタスクを完了しようとするテスト"""
    # 学習項目を作成
    create_response = client.post(
        "/api/learning-items/",
        json={"title": "Item for Double Complete"}
    )
    task_id = create_response.json()["review_tasks"][0]["id"]

    # 1回目の完了
    client.post(f"/api/review-tasks/{task_id}/complete")

    # 2回目の完了（エラーになるべき）
    response = client.post(f"/api/review-tasks/{task_id}/complete")
    assert response.status_code == 400


def test_uncomplete_review_task():
    """復習タスク完了取り消しのテスト"""
    # 学習項目を作成
    create_response = client.post(
        "/api/learning-items/",
        json={"title": "Item for Uncomplete"}
    )
    task_id = create_response.json()["review_tasks"][0]["id"]

    # 完了
    client.post(f"/api/review-tasks/{task_id}/complete")

    # 取り消し
    response = client.post(f"/api/review-tasks/{task_id}/uncomplete")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Ready"
    assert data["completed_at"] is None
