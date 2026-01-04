from datetime import date, timedelta
from typing import List, Dict, Any

# 復習スケジュールの定義（忘却曲線に基づく）
REVIEW_SCHEDULE = [
    ("学習直後", 0),
    ("1日後", 1),
    ("3日後", 3),
    ("1週間後", 7),
    ("2週間後", 14),
    ("1ヶ月後", 30),
    ("3ヶ月後", 90),
    ("半年後", 180),
    ("1年後", 365),
]


def generate_review_tasks(learning_item_id: int, start_date: date) -> List[Dict[str, Any]]:
    """
    学習項目に対する復習タスクを生成する

    Args:
        learning_item_id: 学習項目のID
        start_date: 学習開始日（ユーザーのタイムゾーンで計算された日付）

    Returns:
        生成する復習タスクのリスト
    """
    tasks = []

    for stage_name, offset_days in REVIEW_SCHEDULE:
        due = start_date + timedelta(days=offset_days)

        # Day 0（学習直後）のタスクは自動的にReady状態にする
        status = "Ready" if offset_days == 0 else "Pending"

        tasks.append({
            "learning_item_id": learning_item_id,
            "stage_name": stage_name,
            "stage_offset_days": offset_days,
            "due_date": due,
            "status": status
        })

    return tasks


def generate_next_yearly_task(learning_item_id: int, current_offset_days: int, current_due_date: date) -> Dict[str, Any]:
    """
    1年ごとの復習タスクの次のタスクを生成する

    Args:
        learning_item_id: 学習項目のID
        current_offset_days: 現在のタスクのオフセット日数（365, 730, 1095, ...）
        current_due_date: 現在のタスクの予定日

    Returns:
        次の1年後タスクの辞書
    """
    next_offset = current_offset_days + 365
    next_due_date = current_due_date + timedelta(days=365)
    years = next_offset // 365

    return {
        "learning_item_id": learning_item_id,
        "stage_name": f"{years}年後",
        "stage_offset_days": next_offset,
        "due_date": next_due_date,
        "status": "Pending"
    }
