# gitlab-webhook-receive

GitLabのwebhookを受信してissue番号とdescriptionを標準出力に出力するPythonスクリプトです。

## 機能

- GitLabのissue関連webhookを受信
- issue番号（iid）とdescriptionを標準出力に出力
- issue以外のwebhookも受信可能（ログのみ）

## 使用方法

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. サーバーの起動

```bash
python3 webhook_receiver.py
```

サーバーはデフォルトでポート5000で起動します。

### 3. GitLabでのwebhook設定

GitLabプロジェクトの設定で以下のURLをwebhookとして設定してください：

```
http://your-server:5000/webhook
```

## 出力例

issueのwebhookを受信すると、標準出力に以下の形式で出力されます：

```
Issue Number: 42
Description: これはテスト用のイシューの説明です。
Title: テストイシュー
Action: open
--------------------------------------------------
```

## エンドポイント

- `POST /webhook` - GitLab webhookを受信
- `GET /health` - ヘルスチェック
