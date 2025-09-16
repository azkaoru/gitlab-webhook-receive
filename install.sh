#!/bin/bash

# GitLab Webhook Receiver systemd Installation Script
# For Rocky Linux 9

set -e

INSTALL_DIR="/opt/gitlab-webhook-receive"
CONFIG_DIR="/etc/gitlab-webhook-receive"
SERVICE_FILE="gitlab-webhook-receive.service"
USER="webhook"
GROUP="webhook"

echo "=== GitLab Webhook Receiver systemd Installation ==="

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Create user and group for the service
echo "Creating user and group: $USER"
if ! id "$USER" &>/dev/null; then
    useradd --system --no-create-home --shell /bin/false "$USER"
fi

# Create installation directory
echo "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Copy application files
echo "Copying application files..."
cp webhook_receiver.py "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"
if [ -f README.md ]; then
    cp README.md "$INSTALL_DIR/"
fi

# Set ownership
chown -R "$USER:$GROUP" "$INSTALL_DIR"
chmod 755 "$INSTALL_DIR"
chmod 644 "$INSTALL_DIR"/*.py "$INSTALL_DIR"/*.txt

# Install Python dependencies
echo "Installing Python dependencies..."
cd "$INSTALL_DIR"
pip3 install -r requirements.txt

# Create configuration directory
echo "Creating configuration directory: $CONFIG_DIR"
mkdir -p "$CONFIG_DIR"

# Copy configuration template if config doesn't exist
if [ ! -f "$CONFIG_DIR/config" ]; then
    echo "Creating configuration file template..."
    cp config.example "$CONFIG_DIR/config"
    chmod 600 "$CONFIG_DIR/config"
    chown "$USER:$GROUP" "$CONFIG_DIR/config"
    echo "  Configuration file created at $CONFIG_DIR/config"
    echo "  Please edit this file with your GitLab settings"
fi

# Install systemd service
echo "Installing systemd service..."
cp "$SERVICE_FILE" /etc/systemd/system/
chmod 644 "/etc/systemd/system/$SERVICE_FILE"

# Reload systemd and enable service
echo "Enabling systemd service..."
systemctl daemon-reload
systemctl enable gitlab-webhook-receive.service

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "1. Edit the configuration file: $CONFIG_DIR/config"
echo "2. Start the service: systemctl start gitlab-webhook-receive"
echo "3. Check status: systemctl status gitlab-webhook-receive"
echo "4. View logs: journalctl -u gitlab-webhook-receive -f"
echo ""
echo "The service will listen on port 50000 for GitLab webhooks."