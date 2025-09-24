#!/bin/bash

echo "Starting bypasswaf uninstallation..."

# --- กำหนดค่าพื้นฐาน ---
VENV_DIR="$HOME/.bypasswaf-env"
SCRIPT_LINK="/usr/local/bin/bypasswaf"

# --- ยืนยันก่อนลบ ---
read -p "Are you sure you want to uninstall bypasswaf? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

# --- ลบ symlink ---
if [ -L "$SCRIPT_LINK" ]; then
    echo "Removing symlink at $SCRIPT_LINK ..."
    sudo rm -f "$SCRIPT_LINK"
else
    echo "Symlink $SCRIPT_LINK not found. Skipping..."
fi

# --- ลบ Virtual Environment ---
if [ -d "$VENV_DIR" ]; then
    echo "Removing virtual environment at $VENV_DIR ..."
    rm -rf "$VENV_DIR"
else
    echo "Virtual environment not found at $VENV_DIR. Skipping..."
fi

# --- สรุปผล ---
echo ""
echo "Bypasswaf uninstallation completed!"
echo "All related files have been removed."
