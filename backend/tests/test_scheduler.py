import pytest
from datetime import date, timedelta
from app.scheduler import generate_review_tasks, generate_next_yearly_task


def test_generate_review_tasks():
    """復習タスク生成のテスト"""
    start_date = date(2024, 1, 1)
    tasks = generate_review_tasks(learning_item_id=1, start_date=start_date)

    # 9個のタスクが生成されることを確認
    assert len(tasks) == 9

    # Day 0 (学習直後)
    assert tasks[0]["stage_name"] == "学習直後"
    assert tasks[0]["stage_offset_days"] == 0
    assert tasks[0]["due_date"] == date(2024, 1, 1)
    assert tasks[0]["status"] == "Ready"  # Day 0は自動的にReady

    # Day 1 (1日後)
    assert tasks[1]["stage_name"] == "1日後"
    assert tasks[1]["stage_offset_days"] == 1
    assert tasks[1]["due_date"] == date(2024, 1, 2)
    assert tasks[1]["status"] == "Pending"

    # Day 3 (3日後)
    assert tasks[2]["stage_name"] == "3日後"
    assert tasks[2]["stage_offset_days"] == 3
    assert tasks[2]["due_date"] == date(2024, 1, 4)

    # Day 7 (1週間後)
    assert tasks[3]["stage_name"] == "1週間後"
    assert tasks[3]["stage_offset_days"] == 7
    assert tasks[3]["due_date"] == date(2024, 1, 8)

    # Day 14 (2週間後)
    assert tasks[4]["stage_name"] == "2週間後"
    assert tasks[4]["stage_offset_days"] == 14
    assert tasks[4]["due_date"] == date(2024, 1, 15)

    # Day 30 (1ヶ月後)
    assert tasks[5]["stage_name"] == "1ヶ月後"
    assert tasks[5]["stage_offset_days"] == 30
    assert tasks[5]["due_date"] == date(2024, 1, 31)

    # Day 90 (3ヶ月後)
    assert tasks[6]["stage_name"] == "3ヶ月後"
    assert tasks[6]["stage_offset_days"] == 90
    assert tasks[6]["due_date"] == date(2024, 3, 31)

    # Day 180 (半年後)
    assert tasks[7]["stage_name"] == "半年後"
    assert tasks[7]["stage_offset_days"] == 180
    assert tasks[7]["due_date"] == date(2024, 6, 29)

    # Day 365 (1年後)
    assert tasks[8]["stage_name"] == "1年後"
    assert tasks[8]["stage_offset_days"] == 365
    assert tasks[8]["due_date"] == date(2025, 1, 1)


def test_generate_next_yearly_task():
    """1年後タスクの次タスク生成テスト"""
    # 1年後タスク（365日）の次のタスクを生成
    next_task = generate_next_yearly_task(
        learning_item_id=1,
        current_offset_days=365,
        current_due_date=date(2025, 1, 1)
    )

    assert next_task["stage_name"] == "2年後"
    assert next_task["stage_offset_days"] == 730
    assert next_task["due_date"] == date(2026, 1, 1)
    assert next_task["status"] == "Pending"


def test_generate_next_yearly_task_multiple_years():
    """複数年後タスクの生成テスト"""
    # 2年後タスク（730日）の次のタスクを生成
    next_task = generate_next_yearly_task(
        learning_item_id=1,
        current_offset_days=730,
        current_due_date=date(2026, 1, 1)
    )

    assert next_task["stage_name"] == "3年後"
    assert next_task["stage_offset_days"] == 1095
    assert next_task["due_date"] == date(2027, 1, 1)

    # 5年後タスク（1825日）の次のタスクを生成
    next_task2 = generate_next_yearly_task(
        learning_item_id=1,
        current_offset_days=1825,
        current_due_date=date(2030, 1, 1)
    )

    assert next_task2["stage_name"] == "6年後"
    assert next_task2["stage_offset_days"] == 2190
    assert next_task2["due_date"] == date(2031, 1, 1)


def test_all_tasks_have_learning_item_id():
    """すべてのタスクにlearning_item_idが設定されることを確認"""
    tasks = generate_review_tasks(learning_item_id=42, start_date=date(2024, 1, 1))

    for task in tasks:
        assert task["learning_item_id"] == 42


def test_due_dates_are_in_order():
    """予定日が昇順であることを確認"""
    tasks = generate_review_tasks(learning_item_id=1, start_date=date(2024, 1, 1))

    for i in range(len(tasks) - 1):
        assert tasks[i]["due_date"] < tasks[i + 1]["due_date"]
