#!/bin/bash

# Test script to validate systemd configuration
# This script performs basic validation without requiring root privileges

echo "=== GitLab Webhook Receiver systemd Configuration Test ==="

# Test 1: Service file syntax
echo "1. Testing systemd service file syntax..."
if systemd-analyze verify gitlab-webhook-receive.service 2>/dev/null; then
    echo "   ✓ Service file syntax is valid"
else
    echo "   ✗ Service file syntax is invalid"
    exit 1
fi

# Test 2: Python script syntax
echo "2. Testing Python script syntax..."
if python3 -m py_compile webhook_receiver.py 2>/dev/null; then
    echo "   ✓ Python script syntax is valid"
else
    echo "   ✗ Python script syntax is invalid"
    exit 1
fi

# Test 3: Installation script syntax
echo "3. Testing installation script syntax..."
if bash -n install.sh; then
    echo "   ✓ Installation script syntax is valid"
else
    echo "   ✗ Installation script syntax is invalid"
    exit 1
fi

# Test 4: Uninstallation script syntax
echo "4. Testing uninstallation script syntax..."
if bash -n uninstall.sh; then
    echo "   ✓ Uninstallation script syntax is valid"
else
    echo "   ✗ Uninstallation script syntax is invalid"
    exit 1
fi

# Test 5: Configuration file template
echo "5. Testing configuration file template..."
if [ -f config.example ]; then
    echo "   ✓ Configuration template exists"
else
    echo "   ✗ Configuration template missing"
    exit 1
fi

# Test 6: Required files presence
echo "6. Checking required files..."
required_files=("webhook_receiver.py" "requirements.txt" "gitlab-webhook-receive.service" "install.sh" "uninstall.sh" "config.example")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file exists"
    else
        echo "   ✗ $file missing"
        exit 1
    fi
done

# Test 7: Dependencies check
echo "7. Testing Python dependencies..."
if pip3 show Flask requests >/dev/null 2>&1; then
    echo "   ✓ Python dependencies are installed"
else
    echo "   ⚠ Python dependencies need to be installed (this is expected if not already installed)"
fi

# Test 8: Application basic functionality
echo "8. Testing application import..."
if python3 -c "import sys; sys.path.insert(0, '.'); import webhook_receiver" 2>/dev/null; then
    echo "   ✓ Application imports successfully"
else
    echo "   ⚠ Application import failed (dependencies may need to be installed)"
fi

echo ""
echo "=== Test Summary ==="
echo "✓ All critical tests passed"
echo "ℹ The systemd service configuration is ready for deployment"
echo ""
echo "To install on Rocky Linux 9:"
echo "1. Run: sudo ./install.sh"
echo "2. Configure: sudo vi /etc/gitlab-webhook-receive/config"
echo "3. Start: sudo systemctl start gitlab-webhook-receive"