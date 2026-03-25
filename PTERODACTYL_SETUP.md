# Discord Bot - Pterodactyl Panel Setup Guide

Panduan lengkap untuk menjalankan Discord Bot di **Pterodactyl Panel**.

## 🚀 Quick Start (Pterodactyl Panel)

### 1. Upload Bot ke Panel
- Login ke Pterodactyl Panel
- Buat server baru atau gunakan yang ada
- Upload semua file bot ke direktori `/home/container/`
- File penting:
  - `bot.py`
  - `requirements.txt`
  - `start.sh`
  - `.env` (atau `.env.example`)
  - **Folder: `cogs/`**
  - **Folder: `assets/`**
  - **Folder: `web/`** (Web Dashboard)

### 2. Setup Environment Variables
Di Pterodactyl Panel **Settings → Startup**:

```
DISCORD_TOKEN=your_bot_token_here
GROQ_API_KEY=your_groq_api_key (opsional)
```

### 3. Set Startup Command
Di Pterodactyl Panel **Settings → Startup**:

**Startup Command:**
```bash
bash start.sh
```

Atau jika menggunakan Docker:
```bash
bash start.sh
```

### 4. Optional: Set Image/Docker
Di Pterodactyl Panel, pilih Docker image:
```
python:3.10-slim
```

atau gunakan custom Docker:
```bash
docker build -t discord-bot:latest .
```

### 5. Start Bot
Klik tombol **Start** di Pterodactyl Panel

---

## 📋 File Structure untuk Pterodactyl

```
/home/container/
├── bot.py                    # Main bot file
├── start.sh                  # Startup script (PENTING!)
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── Dockerfile               # Docker configuration
├── cogs/                    # Command modules
│   ├── ai_commands.py
│   ├── music_commands.py
│   ├── moderation_commands.py
│   └── utility_commands.py
├── assets/                  # Images/resources
│   └── banner.jpg
├── web/                     # Web Dashboard
│   ├── app.py              # Flask web server
│   ├── static/             # CSS, JS files
│   └── templates/          # HTML templates
└── bot.log                 # Log file (auto-generated)
```

---

## ⚙️ Configuration di Pterodactyl

### Environment Variables
```
DISCORD_TOKEN        # Required: Your bot token
GROQ_API_KEY        # Optional: For AI features
PORT                 # Optional: Web server port (default: 5000)
PYTHONUNBUFFERED=1  # Recommended: For better logging
```

### Startup Command Settings
```
Command:  bash start.sh
Shutdown: SIGTERM (15 seconds timeout)
```

### Port Allocations
```
Port 5000 (TCP)     # Web Dashboard
```

### Resource Allocation
Recommended untuk Discord Bot:
- **CPU**: 1-2 cores
- **RAM**: 512 MB - 1 GB  (1-2 GB untuk music features)
- **Disk**: 2 GB

---

## 🔍 Troubleshooting Pterodactyl

### Bot stops immediately
```
Solusi:
1. Check logs di Pterodactyl console
2. Pastikan DISCORD_TOKEN set di environment
3. Pastikan start.sh executable: chmod +x start.sh
4. Test manual: python bot.py
```

### Web Dashboard tidak bisa diakses
```
Solusi:
1. Pastikan port 5000 dialokasikan di Pterodactyl
2. Check firewall rules: port 5000 must be open
3. Verify Flask running: grep "\[WEB\]" bot.log
4. Test: curl http://localhost:5000/api/health
```

### Permission denied on start.sh
```bash
# Set execute permission
chmod +x start.sh
chmod -R 755 web/
```

### Python modules not found
```bash
# Install dependencies via console
pip install -r requirements.txt

# Or Pterodactyl akan auto-install saat startup
```

### Bot online but not responding
```
Possible issues:
1. Discord token invalid
2. Bot not added to server
3. Missing intents permission
4. Command prefix wrong (default: !)
5. Check logs for [ERROR] entries
```

### Memory/CPU issues
```
Solutions:
1. Increase allocation di Pterodactyl
2. Disable heavy features (music, AI)
3. Clear old logs: rm bot.log atau truncate bot.log
4. Restart server via Pterodactyl
```

---

## 📊 Monitoring Bot Status

### Via Pterodactyl Console
- **Status**: Green = Online, Red = Offline
- **Memory Usage**: Real-time monitoring
- **Logs**: Live console output

### Via Discord
```
!ping          # Check latency
!info          # Bot information
```

### Log Files
Bot logs tersimpan di:
- **Pterodactyl Console** (live)
- **`bot.log`** file (persistent)

---

## 🌐 Web Dashboard

Bot ini dilengkapi dengan **Web Dashboard** yang berjalan bersamaan dengan bot:

### Akses Dashboard
```
URL: http://<your-pterodactyl-ip>:5000
```

### Fitur Dashboard
- Bot status & statistics
- Commands list
- Real-time monitoring
- Multi-language support (🇬🇧 EN / 🇮🇩 ID)

### Web Server Logs
Web server logs tercatat di:
- **`bot.log`** file (bersama bot logs)
- **Pterodactyl Console** (live output dengan prefix `[WEB]`)

### Log Format
```
2024-01-15 10:30:46,456 | [INFO] | FlaskApp | [WEB] Dashboard access from 192.168.1.1
2024-01-15 10:30:47,789 | [INFO] | FlaskApp | [WEB] Status API request from 192.168.1.1
```

### Debugging Web Server
```bash
# Check if Flask is running
curl http://localhost:5000/api/health

# Check web server logs
tail -f bot.log | grep "\[WEB\]"
```

---

Jika Pterodactyl support Docker:

### Build Image
```bash
docker build -t discord-bot:latest .
```

### Run Container
```bash
docker run -d \
  --name discord-bot \
  -e DISCORD_TOKEN="your_token" \
  -e GROQ_API_KEY="your_key" \
  -v /data/bot:/app \
  discord-bot:latest
```

### Check Logs
```bash
docker logs -f discord-bot
```

---

## 🔐 Security Tips

1. **Protect .env file**
   ```bash
   chmod 600 .env
   ```

2. **Don't commit .env to git**
   - Already in `.gitignore`

3. **Keep token secret**
   - Regenerate token jika leaked
   - Developer Portal → Settings → Reset Token

4. **Use strong permissions**
   - Give bot minimal required permissions
   - Check Discord OAuth2 settings

5. **Monitor logs for errors**
   - Check Pterodactyl logs regularly
   - Look for suspicious activity

---

## 📝 .env Template untuk Pterodactyl

```env
# Required
DISCORD_TOKEN=your_bot_token_from_discord_dev_portal

# Optional - AI Features
GROQ_API_KEY=your_groq_api_key

# Recommended for logging
PYTHONUNBUFFERED=1
```

---

## 🎯 Pre-Flight Checklist

Sebelum start bot di Pterodactyl:

- [ ] Bot file uploaded (`bot.py`, `cogs/`, `assets/`, `web/`)
- [ ] `requirements.txt` uploaded
- [ ] `start.sh` uploaded
- [ ] `.env` file created dengan DISCORD_TOKEN
- [ ] Startup command set: `bash start.sh`
- [ ] Environment variables configured
- [ ] Port 5000 allocated for web dashboard
- [ ] Sufficient resources allocated
- [ ] Bot invited to Discord server
- [ ] Intents enabled di Discord dev portal
- [ ] Flask dependencies in `requirements.txt`

---

## 📚 Related Guides

- [Pterodactyl Official Docs](https://pterodactyl.io/)
- [Discord.py Docs](https://discordpy.readthedocs.io/)
- [Main Bot Setup](README.md)
- [Node.js Wrapper Guide](README_NODEJS.md)

---

**Version**: 2.1  
**Last Updated**: March 2026  
**Support**: Python 3.10+, Pterodactyl Panel 1.0+
