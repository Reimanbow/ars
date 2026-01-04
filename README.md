# Active Recall Scheduler (ARS)

忘却曲線に基づいた復習スケジュール管理アプリケーション

## 概要

Active Recall Scheduler (ARS) は、エビングハウスの忘却曲線に基づいて、学習内容の復習タイミングを自動的に管理するWebアプリケーションです。

### 主な機能

- **学習項目の登録**: 新しく学習した内容を登録
- **自動復習スケジュール生成**: 登録時に9段階の復習タスクを自動生成
- **今日の復習タスク表示**: 実施すべき復習をダッシュボードに表示
- **復習進捗の可視化**: 各学習項目の復習状況をロードマップ形式で表示
- **1年後以降の自動継続**: 1年後タスク完了時に次の1年後タスクを自動生成

### 復習スケジュール

以下のタイミングで復習タスクが生成されます:

1. **学習直後** (Day 0)
2. **1日後** (Day 1)
3. **3日後** (Day 3)
4. **1週間後** (Day 7)
5. **2週間後** (Day 14)
6. **1ヶ月後** (Day 30)
7. **3ヶ月後** (Day 90)
8. **半年後** (Day 180)
9. **1年後** (Day 365)
10. **以降、1年ごと** (Day 730, Day 1095, ...)

## 技術スタック

- **バックエンド**: Python 3.11 + FastAPI
- **データベース**: SQLite
- **フロントエンド**: Vanilla JavaScript + Tailwind CSS
- **開発環境**: Docker + Docker Compose

## セットアップ

### 前提条件

- Docker
- Docker Compose

### 初回セットアップ

1. リポジトリのクローン（またはファイルの配置）

```bash
cd /home/yamazaki/ars
```

2. 環境変数ファイルの確認

```bash
# .env ファイルが存在することを確認
ls -la .env
```

3. Dockerイメージのビルド

```bash
docker-compose build
```

### アプリケーションの起動

```bash
docker-compose up
```

起動後、以下のURLでアクセスできます:

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API文書（Swagger UI）**: http://localhost:8000/docs

### アプリケーションの停止

```bash
# Ctrl+C で停止、またはバックグラウンド実行の場合:
docker-compose down
```

## 使い方

### 1. 学習項目の登録

1. ダッシュボード (http://localhost:3000) にアクセス
2. 「+ 新しい学習項目を追加」ボタンをクリック
3. タイトルと内容を入力して「作成」ボタンをクリック
4. 自動的に9個の復習タスクが生成されます

### 2. 今日の復習を実施

1. ダッシュボードに表示される「今日の復習タスク」を確認
2. アクティブリコール（想起練習）を実施
3. 「完了」ボタンをクリックして記録

### 3. 復習進捗の確認

1. 「学習項目一覧」ページに移動
2. 確認したい学習項目をクリック
3. 復習進捗ロードマップで各ステージの状態を確認

## プロジェクト構造

```
/home/yamazaki/ars/
├── docker-compose.yml          # Docker Compose設定
├── .env                        # 環境変数
├── backend/                    # バックエンド
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 # FastAPIアプリケーション
│   └── app/
│       ├── config.py           # 設定
│       ├── database.py         # DB接続
│       ├── models.py           # データモデル
│       ├── schemas.py          # Pydanticスキーマ
│       ├── crud.py             # CRUD操作
│       ├── scheduler.py        # 復習スケジュール生成
│       └── api/
│           ├── learning_items.py  # 学習項目API
│           └── review_tasks.py    # 復習タスクAPI
├── frontend/                   # フロントエンド
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html              # ダッシュボード
│   ├── items.html              # 学習項目一覧
│   ├── item-detail.html        # 学習項目詳細
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── config.js
│       ├── api.js              # API呼び出し
│       ├── dashboard.js
│       ├── items.js
│       └── item-detail.js
├── data/                       # SQLiteデータベース保存先
└── docs/
    └── SPEC.md                 # 仕様書
```

## APIエンドポイント

### 学習項目

- `POST /api/learning-items/` - 新規学習項目の作成
- `GET /api/learning-items/` - 学習項目一覧の取得
- `GET /api/learning-items/{id}` - 学習項目詳細の取得
- `PUT /api/learning-items/{id}` - 学習項目の更新
- `DELETE /api/learning-items/{id}` - 学習項目の削除

### 復習タスク

- `GET /api/review-tasks/today` - 今日の復習タスク一覧
- `GET /api/review-tasks/{id}` - 復習タスク詳細
- `POST /api/review-tasks/{id}/complete` - 復習タスクの完了
- `POST /api/review-tasks/{id}/uncomplete` - 復習タスクの完了取り消し

詳細は http://localhost:8000/docs を参照してください。

## テスト

```bash
# バックエンドのテストを実行
docker-compose exec backend pytest
```

## トラブルシューティング

### ポートが既に使用されている

```bash
# 8000番ポートまたは3000番ポートを使用している他のプロセスを停止してください
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### データベースをリセットしたい

```bash
# data ディレクトリ内の .db ファイルを削除
rm data/*.db

# コンテナを再起動
docker-compose restart backend
```

### コンテナが起動しない

```bash
# ログを確認
docker-compose logs backend
docker-compose logs frontend

# コンテナを再ビルド
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## ライセンス

MIT License

## 貢献

バグ報告や機能リクエストは Issue でお願いします。

## 参考

- [仕様書](docs/SPEC.md)
- FastAPI: https://fastapi.tiangolo.com/
- Tailwind CSS: https://tailwindcss.com/
