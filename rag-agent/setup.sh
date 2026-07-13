#!/bin/bash
# Oracle Cloud Ubuntu setup — run from inside aw-trading/rag-agent/
set -e

echo "=== Installing system dependencies ==="
sudo apt update && sudo apt install -y python3-pip python3-venv git ffmpeg

echo "=== Setting up Python environment ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Installing Python packages ==="
pip install -r requirements.txt

echo "=== Installing systemd service ==="
# Patch WorkingDirectory to the current directory
sed "s|WorkingDirectory=.*|WorkingDirectory=$(pwd)|; s|ExecStart=.*|ExecStart=$(pwd)/venv/bin/python bot.py|" \
    aw-bot.service | sudo tee /etc/systemd/system/aw-bot.service > /dev/null
sudo systemctl daemon-reload

echo ""
echo "=== Setup complete ==="
echo "Next steps:"
echo "1. Create .env:   cp .env.example .env && nano .env"
echo "2. Run ingest:    python ingest.py   (takes a while — use tmux)"
echo "3. Start bot:     sudo systemctl enable --now aw-bot"
echo "4. Check status:  sudo systemctl status aw-bot"
