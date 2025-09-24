#!/bin/bash

echo "Starting bypasswaf installation..."

# --- ตรวจสอบ Python3 ---
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing..."
    sudo apt update && sudo apt install -y python3 python3-venv python3-pip dos2unix
fi

# --- ติดตั้ง Chromium และ Chromium driver ---
echo "Installing Chromium and Chromedriver..."
sudo apt update
sudo apt install -y chromium-browser chromium-chromedriver

# --- ตรวจสอบว่า chromium และ chromedriver ติดตั้งถูกต้องหรือไม่ ---
echo "Checking installed versions..."
chromium-browser --version
chromedriver --version

# --- สร้าง symlink ถ้าจำเป็น เพื่อให้ selenium หา chromium เจอ ---
if [ ! -f "/usr/bin/chromium" ]; then
    echo "Creating symlink for chromium binary..."
    sudo ln -s /usr/bin/chromium-browser /usr/bin/chromium
fi

# --- ตรวจสอบไฟล์ bypasswaf.py ---
SCRIPT_NAME="bypasswaf.py"
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "Error: '$SCRIPT_NAME' not found in current directory."
    echo "Please make sure '$SCRIPT_NAME' exists here."
    exit 1
fi

# --- แปลงไฟล์ Python จาก CRLF (Windows) เป็น LF (Linux) ---
echo "Converting line endings to Linux format..."
dos2unix "$SCRIPT_NAME"

# --- สร้างโฟลเดอร์สำหรับติดตั้งโปรแกรม ---
INSTALL_DIR="/usr/local/share/bypasswaf"
sudo mkdir -p "$INSTALL_DIR"

# --- ย้ายไฟล์โปรแกรมหลักไปยัง INSTALL_DIR ---
echo "Moving bypasswaf.py to $INSTALL_DIR ..."
sudo cp "$SCRIPT_NAME" "$INSTALL_DIR/"

# --- สร้าง Virtual Environment ---
VENV_DIR="$HOME/.bypasswaf-env"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment at $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
fi

# --- ติดตั้ง dependencies ภายใน Virtual Environment ---
echo "Installing Python dependencies in virtual environment..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install requests pytz colorama cryptography beautifulsoup4 selenium
deactivate

# --- สร้าง wrapper script สำหรับรัน bypasswaf ---
WRAPPER="/usr/local/bin/bypasswaf"
echo "#!/bin/bash" | sudo tee $WRAPPER > /dev/null
echo "source \"$VENV_DIR/bin/activate\"" | sudo tee -a $WRAPPER > /dev/null
echo "python \"$INSTALL_DIR/$SCRIPT_NAME\" \"\$@\"" | sudo tee -a $WRAPPER > /dev/null
echo "deactivate" | sudo tee -a $WRAPPER > /dev/null
sudo chmod +x $WRAPPER

# --- สรุปผลการติดตั้ง ---
echo ""
echo "Installation completed!"
echo "You can now run 'bypasswaf' from any terminal without modifying bypasswaf.py."
echo ""
echo "Program installed to: $INSTALL_DIR"
echo "Virtual environment is stored at: $VENV_DIR"
echo ""
echo "Example usage:"
echo "  bypasswaf -t TARGET"
echo "  bypasswaf -s SECURITYTRAILSAPI"
echo "  bypasswaf -w WORDLISTS"
