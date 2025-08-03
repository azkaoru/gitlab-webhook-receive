# gitlab-webhook-receive

GitLabのwebhookを受信してissue番号とdescriptionを標準出力に出力するPythonスクリプトです。

## 機能

- GitLabのissue関連webhookを受信
- issue番号（iid）とdescriptionを標準出力に出力
- issue情報でGitLabパイプラインをトリガー
- issue以外のwebhookも受信可能（ログのみ）

## 使用方法

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

GitLabパイプラインのトリガー機能を使用する場合は、以下の環境変数を設定してください：

```bash
export PROJECT_ID="123456"                    # GitLabプロジェクトID
export TOKEN="your_trigger_token_here"        # パイプライントリガートークン
export REF="main"                             # トリガーするブランチ/タグ
```

### 3. サーバーの起動

```bash
python3 webhook_receiver.py
```

サーバーはデフォルトでポート5000で起動します。

### 4. GitLabでのwebhook設定

GitLabプロジェクトの設定で以下のURLをwebhookとして設定してください：

```
http://your-server:5000/webhook
```

## 出力例

issueのwebhookを受信すると、以下が実行されます：

1. 標準出力に以下の形式で出力されます：

```
Issue Number: 42
Description: これはテスト用のイシューの説明です。
Title: テストイシュー
Action: open
--------------------------------------------------
```

2. 環境変数が設定されている場合、以下の形式でGitLabパイプラインがトリガーされます：

**トリガーURL：**
```
POST https://gitlab.example.com/api/v4/projects/{PROJECT_ID}/trigger/pipeline?token={TOKEN}&ref={REF}
```

**パイプライン変数：**
- `ISSUE_NUMBER`: issue番号
- `ISSUE_DESCRIPTION`: issueの説明
- `ISSUE_TITLE`: issueのタイトル  
- `ISSUE_ACTION`: issueのアクション（open, close等）

## エンドポイント

- `POST /webhook` - GitLab webhookを受信
- `GET /health` - ヘルスチェック

## 環境変数

- `PROJECT_ID` - GitLabプロジェクトID（パイプライントリガー用）
- `TOKEN` - GitLabパイプライントリガートークン
- `REF` - トリガーするブランチまたはタグ名
