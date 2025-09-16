#!/bin/bash

# GitLab Webhook Receiver systemd Uninstallation Script
# For Rocky Linux 9

set -e

INSTALL_DIR="/opt/gitlab-webhook-receive"
CONFIG_DIR="/etc/gitlab-webhook-receive"
SERVICE_FILE="gitlab-webhook-receive.service"
USER="webhook"

echo "=== GitLab Webhook Receiver systemd Uninstallation ==="

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Stop and disable service
echo "Stopping and disabling service..."
if systemctl is-active --quiet gitlab-webhook-receive; then
    systemctl stop gitlab-webhook-receive
fi

if systemctl is-enabled --quiet gitlab-webhook-receive; then
    systemctl disable gitlab-webhook-receive
fi

# Remove systemd service file
echo "Removing systemd service file..."
if [ -f "/etc/systemd/system/$SERVICE_FILE" ]; then
    rm "/etc/systemd/system/$SERVICE_FILE"
fi

# Reload systemd
systemctl daemon-reload

# Ask about removing configuration
echo ""
read -p "Remove configuration directory $CONFIG_DIR? [y/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$CONFIG_DIR"
    echo "Configuration directory removed"
fi

# Ask about removing installation directory
echo ""
read -p "Remove installation directory $INSTALL_DIR? [y/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$INSTALL_DIR"
    echo "Installation directory removed"
fi

# Ask about removing user
echo ""
read -p "Remove user $USER? [y/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if id "$USER" &>/dev/null; then
        userdel "$USER"
        echo "User $USER removed"
    fi
fi

echo ""
echo "=== Uninstallation Complete ==="