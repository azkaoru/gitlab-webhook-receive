# systemd Setup Guide for GitLab Webhook Receiver

This guide provides step-by-step instructions for setting up the GitLab Webhook Receiver as a systemd service on Rocky Linux 9.

## Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/azkaoru/gitlab-webhook-receive.git
   cd gitlab-webhook-receive
   ```

2. **Install as systemd service**
   ```bash
   sudo ./install.sh
   ```

3. **Configure environment variables**
   ```bash
   sudo vi /etc/gitlab-webhook-receive/config
   ```
   
   Set your GitLab configuration:
   ```bash
   GITLAB_URL=https://your-gitlab.example.com
   PROJECT_ID=your_project_id
   TOKEN=your_trigger_token
   REF=main
   ```

4. **Start the service**
   ```bash
   sudo systemctl start gitlab-webhook-receive
   sudo systemctl enable gitlab-webhook-receive
   ```

5. **Verify it's running**
   ```bash
   sudo systemctl status gitlab-webhook-receive
   curl http://localhost:50000/health
   ```

## Service Management

- **Start**: `sudo systemctl start gitlab-webhook-receive`
- **Stop**: `sudo systemctl stop gitlab-webhook-receive`
- **Restart**: `sudo systemctl restart gitlab-webhook-receive`
- **Status**: `sudo systemctl status gitlab-webhook-receive`
- **Enable auto-start**: `sudo systemctl enable gitlab-webhook-receive`
- **Disable auto-start**: `sudo systemctl disable gitlab-webhook-receive`

## Log Management

View logs with journalctl:

```bash
# Follow logs in real-time
sudo journalctl -u gitlab-webhook-receive -f

# View recent logs
sudo journalctl -u gitlab-webhook-receive --since "1 hour ago"

# View all logs
sudo journalctl -u gitlab-webhook-receive

# Filter by log level
sudo journalctl -u gitlab-webhook-receive -p err
```

## Security Features

The systemd service includes security hardening:
- Runs as dedicated `webhook` user (non-root)
- Private temporary directory
- Protected system directories
- No new privileges allowed

## File Locations

- **Service file**: `/etc/systemd/system/gitlab-webhook-receive.service`
- **Application**: `/opt/gitlab-webhook-receive/`
- **Configuration**: `/etc/gitlab-webhook-receive/config`
- **Logs**: Available via `journalctl` (systemd journal)

## Troubleshooting

1. **Service won't start**
   ```bash
   sudo systemctl status gitlab-webhook-receive
   sudo journalctl -u gitlab-webhook-receive
   ```

2. **Permission issues**
   ```bash
   sudo chown -R webhook:webhook /opt/gitlab-webhook-receive
   sudo chmod 600 /etc/gitlab-webhook-receive/config
   ```

3. **Port conflicts**
   - The service listens on port 50000
   - Check if port is available: `sudo netstat -tlnp | grep 50000`

4. **Configuration issues**
   - Verify config file: `/etc/gitlab-webhook-receive/config`
   - Logs will show missing environment variable warnings

## Uninstallation

To remove the service and all files:
```bash
sudo ./uninstall.sh
```