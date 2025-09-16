# gitlab-webhook-receive

GitLabのwebhookを受信してissue番号とdescriptionを標準出力に出力するPythonスクリプトです。

## 機能

- GitLabのissue関連webhookを受信
- issue番号（iid）、description、assignee_usernameを標準出力に出力
- issue情報でGitLabパイプラインをトリガー
- issue以外のwebhookも受信可能（ログのみ）
- issue_tagで前方一致するラベルを抽出してパイプライン変数として利用可能

## 使用方法

### 方法1: systemdサービスとして実行（推奨）

Rocky Linux 9での本格的な運用に適しています。

#### インストール

```bash
# リポジトリをクローン
git clone https://github.com/azkaoru/gitlab-webhook-receive.git
cd gitlab-webhook-receive

# rootユーザーでインストールスクリプトを実行
sudo ./install.sh
```

#### 設定

```bash
# 設定ファイルを編集
sudo vi /etc/gitlab-webhook-receive/config
```

設定ファイルの例：
```bash
GITLAB_URL=https://gitlab.example.com
PROJECT_ID=123456
TOKEN=your_trigger_token_here
REF=main
```

TOKENはgitlabのProject -> Setting -> CI/CD -> Pipeline trigger tokensより、トークンを発行すること

#### サービス管理

```bash
# サービス開始
sudo systemctl start gitlab-webhook-receive

# サービス停止
sudo systemctl stop gitlab-webhook-receive

# サービス再起動
sudo systemctl restart gitlab-webhook-receive

# サービス状態確認
sudo systemctl status gitlab-webhook-receive

# 自動起動有効化
sudo systemctl enable gitlab-webhook-receive

# ログ確認
sudo journalctl -u gitlab-webhook-receive -f
```

#### アンインストール

```bash
sudo ./uninstall.sh
```

### 方法2: 直接実行（開発・テスト用）

#### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

#### 2. 環境変数の設定

GitLabパイプラインのトリガー機能を使用する場合は、以下の環境変数を設定してください：

```bash
# GitLabサーバーのURL
export GITLAB_URL=https://gitlab.example.com
# GitLabプロジェクトID
export PROJECT_ID=123456
# パイプライントリガートークン
export TOKEN="your_trigger_token_here"
# トリガーするブランチ/タグ
export REF=main
```

#### 3. サーバーの起動

```bash
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

## systemdでのログ管理

systemdサービスとして実行した場合、ログはsystemdジャーナルに記録されます：

```bash
# リアルタイムでログを表示
sudo journalctl -u gitlab-webhook-receive -f

# 過去のログを表示
sudo journalctl -u gitlab-webhook-receive

# 特定の時間以降のログを表示
sudo journalctl -u gitlab-webhook-receive --since "1 hour ago"

# エラーレベルのログのみ表示
sudo journalctl -u gitlab-webhook-receive -p err

# ログの詳細情報も表示
sudo journalctl -u gitlab-webhook-receive -o verbose
```

## 環境変数

- `GITLAB_URL` - GitLabサーバーのURL（例：https://gitlab.example.com）
- `PROJECT_ID` - GitLabプロジェクトID（パイプライントリガー用）
- `TOKEN` - GitLabパイプライントリガートークン
- `REF` - トリガーするブランチまたはタグ名
