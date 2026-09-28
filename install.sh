#!/usr/bin/env bash
set -e

PYTHON_VERSION="3.14.7"

echo "=== 1. Updating APT sources for archived Debian Bullseye packages ==="
# Backup original sources.list
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# Point security repository to the Debian archive server
sudo sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list
sudo sed -i 's|bullseye-security|bullseye-security main|g' /etc/apt/sources.list

echo "=== 2. Refreshing package lists ==="
sudo apt-get update -o Acquire::Check-Valid-Until=false || true

echo "=== 3. Installing system build dependencies ==="
sudo apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  wget \
  curl \
  llvm \
  libncursesw5-dev \
  xz-utils \
  tk-dev \
  libxml2-dev \
  libxmlsec1-dev \
  libffi-dev \
  liblzma-dev \
  git

echo "=== 4. Set pyenv source ==="
# Configure pyenv environment variables for the current script session
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Append to .bashrc so future terminal sessions automatically recognize pyenv
PROFILE_FILE="$HOME/.bashrc"
if ! grep -q 'PYENV_ROOT' "$PROFILE_FILE"; then
  echo '' >> "$PROFILE_FILE"
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "$PROFILE_FILE"
  echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> "$PROFILE_FILE"
  echo 'eval "$(pyenv init -)"' >> "$PROFILE_FILE"
fi

echo "=== 5. Checking for pyenv installation ==="
if ! command -v pyenv &> /dev/null; then
  echo "pyenv not found. Installing pyenv..."
  curl https://pyenv.run | bash

  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init -)"

  PROFILE_FILE="$HOME/.bashrc"
  if ! grep -q 'PYENV_ROOT' "$PROFILE_FILE"; then
    echo '' >> "$PROFILE_FILE"
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "$PROFILE_FILE"
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> "$PROFILE_FILE"
    echo 'eval "$(pyenv init -)"' >> "$PROFILE_FILE"
    echo "Added pyenv environment configuration to $PROFILE_FILE"
  fi
else
  echo "pyenv is already installed."
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init -)"
fi

echo "=== 6. Building Python $PYTHON_VERSION without ensurepip ==="
CPPFLAGS="-I/usr/include/openssl" \
LDFLAGS="-L/usr/lib" \
PYTHON_CONFIGURE_OPTS="--without-ensurepip" \
pyenv install "$PYTHON_VERSION" --force

echo "=== 7. Setting local/global pyenv version ==="
pyenv local "$PYTHON_VERSION" || pyenv global "$PYTHON_VERSION"

echo "=== 8. Bootstrapping pip manually ==="
curl -sS https://bootstrap.pypa.io/get-pip.py | python

echo "=== 9. Downloading additional requirements ==="
sudo apt-get install python3-tk
pip install -r requirements.txt

echo "=== Installation complete! ==="
python --version
pip --version

