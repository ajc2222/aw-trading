# RAG Bot Progress

## What's Done

### Bot (bot.py)
- Discord bot running with mention-based interface (`@AW Bot your question`)
- Searches all creators combined, returns best answer + source link with timestamp
- Uses **Gemini** for embeddings, **Groq (llama-3.3-70b)** for answer generation — both free
- Error handling so failures show in Discord instead of silently dying

### Ingestion (ingest.py)
- Automatically tries YouTube captions first, falls back to **Whisper** (local, free) for channels without captions
- Timestamps tracked per chunk — source links jump to the exact point in the video
- `--force` flag deletes existing entries before re-indexing (for re-ingesting with new format)
- Rate limiting (0.7s delay) to stay within Gemini free tier

### Creators indexed
| Creator | Status | Notes |
|---------|--------|-------|
| Flux Trades | ⚠️ Needs re-ingest | Indexed without timestamps |
| Aidenomics | ⚠️ Needs re-ingest | Indexed without timestamps |
| BionicNQ | ⚠️ Needs re-ingest | Indexed without timestamps |
| GXT | ❌ Skipped | Captions fully disabled, no solution |
| TTrades | ❌ Not indexed | Needs Whisper (~196 videos, long) |
| AW Trading | 🔄 Partial | ~7/15 done, needs --force to re-ingest with timestamps |
| ICT | ❌ Not indexed | Needs Whisper (~41 videos) |

### Deploy files
- `requirements.txt` — all dependencies
- `.env.example` — template for API keys
- `setup.sh` — one-command server setup (auto-patches service file paths)
- `aw-bot.service` — systemd service (auto-restart on crash/reboot)

---

## Deploy to Oracle Cloud (free, 24/7)

### One-time setup (you do this)
1. Sign up at **cloud.oracle.com** (card required, won't be charged)
2. Create **ARM Ampere A1** VM → Always Free → Ubuntu 22.04
3. Download SSH key when prompted
4. Open port 443 in the security list (for outbound HTTPS)

### SSH + deploy
```bash
ssh -i your-key.key ubuntu@YOUR_SERVER_IP
git clone https://github.com/ajc2222/aw-trading.git
cd aw-trading/rag-agent
bash setup.sh
cp .env.example .env
nano .env   # paste your 3 keys
```

### Ingest on the server (run in tmux so it survives disconnect)
```bash
tmux new -s ingest
source venv/bin/activate

# Re-ingest stale creators with timestamps
python ingest.py --source flux_trades --force
python ingest.py --source aidenomics --force
python ingest.py --source bionic_nq --force

# Ingest AW Trading fresh
python ingest.py --source aw_trading --force

# Ingest TTrades + ICT via Whisper (very long — leave overnight)
python ingest.py --source ttrades
python ingest.py --source ict
```

### Start the bot
```bash
sudo systemctl enable --now aw-bot
sudo systemctl status aw-bot
```

---

## API Keys (stored in .env — never commit this file)
- `GEMINI_API_KEY` — Google AI Studio (embeddings only)
- `GROQ_API_KEY` — Groq console (answer generation, free)
- `DISCORD_TOKEN` — Discord Developer Portal, bot: AW Bot (client ID: 1526025392404566187)
