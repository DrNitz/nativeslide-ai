#!/usr/bin/env bash
# ==============================================================================
# NativeSlide AI — Oracle Cloud Always Free Ubuntu Instance Setup Script
# Installs Python 3.11, Nginx, Certbot, systemd service, and firewall rules
# ==============================================================================
set -euo pipefail

echo "=========================================================="
echo " Starting NativeSlide AI Oracle Cloud Server Provisioning "
echo "=========================================================="

# 1. System updates & core dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx certbot python3-certbot-nginx curl ufw

# 2. Install uv (ultra-fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# 3. Create app directory
APP_DIR="/var/www/nativeslide-ai"
sudo mkdir -p "$APP_DIR"
sudo chown -R "$USER:$USER" "$APP_DIR"

echo "Directory created at $APP_DIR"

# 4. Clone or copy project into APP_DIR (placeholder step)
# git clone https://github.com/DrNitz/nativeslide-ai.git "$APP_DIR"

# 5. Create Python Virtual Environment
python3.11 -m venv "$APP_DIR/backend/.venv"
source "$APP_DIR/backend/.venv/bin/activate"

# 6. Install Python dependencies
if [ -f "$APP_DIR/backend/requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r "$APP_DIR/backend/requirements.txt"
fi

# 7. Create Systemd Service
sudo tee /etc/systemd/system/nativeslide.service > /dev/null <<EOF
[Unit]
Description=NativeSlide AI FastAPI Backend Engine
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR/backend
EnvironmentFile=$APP_DIR/backend/.env
ExecStart=$APP_DIR/backend/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
# sudo systemctl enable nativeslide
# sudo systemctl start nativeslide

# 8. Configure Nginx Reverse Proxy
sudo tee /etc/nginx/sites-available/nativeslide > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    client_max_body_size 30M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/nativeslide /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# 9. Firewall rules
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
echo "y" | sudo ufw enable

echo "=========================================================="
echo " NativeSlide AI Server Setup Complete!                    "
echo " Backend running on port 8000 via Nginx reverse proxy     "
echo "=========================================================="
