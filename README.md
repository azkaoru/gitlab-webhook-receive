# gitlab-webhook-receive

GitLabのwebhookを受信してissue番号とdescriptionを標準出力に出力するPythonスクリプトです。

## 機能

- GitLabのissue関連webhookを受信
- issue番号（iid）、description、assignee_usernameを標準出力に出力
- issue情報でGitLabパイプラインをトリガー
- issue以外のwebhookも受信可能（ログのみ）
- issue_tagで前方一致するラベルを抽出してパイプライン変数として利用可能

## 使用方法

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

GitLabパイプラインのトリガー機能を使用する場合は、以下の環境変数を設定してください：

```bash
# GitLabサーバーのURL
export GITLAB_URL=https://gitlab.example.com
# GitLabプロジェクトID
export PROJECT_ID=123456
# パイプライントリガートークン
export TOKEN="your_trigger_token_here"
# トリガーするブランチ/タグ
export REF=main"
```

TOKENはgitlabのProject -> Setting -> CI/CD -> Pipeline trigger  tokensより、トークンを発行すること

### 3. サーバーの起動

```bash
source vars
python3 webhook_receiver.py
```

サーバーはデフォルトでポート50000で起動します。

### 4. GitLabでのwebhook設定

GitLabプロジェクトの設定で以下のURLをwebhookとして設定してください：

```
http://your-server:50000/webhook
```

## 出力例

issueのwebhookを受信すると、以下が実行されます：

1. 標準出力に以下の形式で出力されます：

```
Issue Number: 42
Description: これはテスト用のイシューの説明です。
Title: テストイシュー
Action: open
Assignee Username: test_assignee
Issue Tag 1: issue_tag_frontend
Issue Tag 2: issue_tag_backend
--------------------------------------------------
```

2. 環境変数が設定されている場合、以下の形式でGitLabパイプラインがトリガーされます：

**トリガーURL：**
```
POST {GITLAB_URL}/api/v4/projects/{PROJECT_ID}/trigger/pipeline?token={TOKEN}&ref={REF}
```

**パイプライン変数：**
- `ISSUE_NUMBER`: issue番号
- `ISSUE_DESCRIPTION`: issueの説明
- `ISSUE_TITLE`: issueのタイトル  
- `ISSUE_ACTION`: issueのアクション（open, close等）
- `ASSIGNEE_USERNAME`: issueの担当者ユーザー名（未設定の場合は "No assignee"）
- `ISSUE_TAG1`: issue_tagで前方一致するラベルの1つ目（見つからない場合は空文字）
- `ISSUE_TAG2`: issue_tagで前方一致するラベルの2つ目（見つからない場合は空文字）

## エンドポイント

- `POST /webhook` - GitLab webhookを受信
- `GET /health` - ヘルスチェック

## 環境変数

- `GITLAB_URL` - GitLabサーバーのURL（例：https://gitlab.example.com）
- `PROJECT_ID` - GitLabプロジェクトID（パイプライントリガー用）
- `TOKEN` - GitLabパイプライントリガートークン
- `REF` - トリガーするブランチまたはタグ名
