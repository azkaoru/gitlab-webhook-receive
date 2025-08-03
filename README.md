# gitlab-webhook-receive

GitLabのwebhookを受信してissue番号とdescriptionを標準出力に出力するPythonスクリプトです。

## 機能

- GitLabのissue関連webhookを受信
- issue番号（iid）とdescriptionを標準出力に出力
- issue番号とdescriptionを設定されたwebhook URLに転送
- issue以外のwebhookも受信可能（ログのみ）

## 使用方法

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

webhook転送機能を使用する場合は、転送先のwebhook URLを環境変数で設定してください：

```bash
export WEBHOOK_URL="https://your-destination-webhook-url/webhook"
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

2. WEBHOOK_URLが設定されている場合、以下のJSON形式で転送先webhookに送信されます：

```json
{
  "issue_number": 42,
  "description": "これはテスト用のイシューの説明です。",
  "title": "テストイシュー",
  "action": "open"
}
```

## エンドポイント

- `POST /webhook` - GitLab webhookを受信
- `GET /health` - ヘルスチェック

## 環境変数

- `WEBHOOK_URL` - issue情報を転送するwebhookのURL（オプション）
