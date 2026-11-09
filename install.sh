#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$APP_DIR/.venv"

echo "Installing Debian 13 system dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-tk

echo "Creating project virtual environment..."
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r "$APP_DIR/requirements.txt"

echo "Creating desktop shortcut..."
DESKTOP_DIR="$HOME/Desktop"
mkdir -p "$DESKTOP_DIR"
DESKTOP_FILE="$DESKTOP_DIR/photon.desktop"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Photon Team 6
Comment=Launch Photon Application
Exec="$VENV_DIR/bin/python" "$APP_DIR/main.py"
Path=$APP_DIR
Terminal=true
Categories=Development;
EOF

chmod +x "$DESKTOP_FILE"
if command -v gio >/dev/null 2>&1; then
  gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null || true
fi

echo "Installation complete."
echo "Run the application with: $VENV_DIR/bin/python $APP_DIR/main.py"
echo "Desktop shortcut created at: $DESKTOP_FILE"
