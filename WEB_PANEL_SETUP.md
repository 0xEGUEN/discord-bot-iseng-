# Web Dashboard + Pterodactyl Panel Setup

**Status**: ✅ Siap Produksi untuk Pterodactyl Panel

---

## 📋 Perubahan yang Dilakukan

### 1. **Web Server Logging** (`web/app.py`)
- ✅ Tambah logging ke Flask app
- ✅ All requests dicatat di `bot.log` dengan prefix `[WEB]`
- ✅ Log format konsisten dengan Discord bot

**Contoh log:**
```
2024-01-15 10:30:46,456 | [INFO] | FlaskApp | [WEB] Dashboard access from 192.168.1.1 - Language: en
2024-01-15 10:30:47,789 | [INFO] | FlaskApp | [WEB] Status API request from 192.168.1.1
2024-01-15 10:30:48,123 | [INFO] | FlaskApp | [WEB] Health check from 192.168.1.1
```

### 2. **Startup Script Enhancement** (`start.sh`)
- ✅ Web server berjalan di background (port 5000)
- ✅ Discord bot berjalan di foreground (monitored by Pterodactyl)
- ✅ Auto cleanup saat process terminate
- ✅ Logging untuk kedua service

**Flow:**
```bash
start.sh
├── Check .env file
├── Check Python installation
├── Install dependencies
├── START: Web Server (Background) → Port 5000
├── START: Discord Bot (Foreground) → Monitored
└── Both log to: bot.log
```

### 3. **Pterodactyl Configuration Updates**
- ✅ `PTERODACTYL_CONFIG.md` - Added port config & web server docs
- ✅ `PTERODACTYL_SETUP.md` - Added web dashboard section
- ✅ Environment variables untuk custom PORT
- ✅ Troubleshooting untuk web server

---

## 🚀 Cara Menjalankan di Pterodactyl Panel

### Step 1: Upload Files
```
Upload semua folder ke Pterodactyl:
✅ bot.py
✅ start.sh (PENTING!)
✅ requirements.txt
✅ .env (atau .env.example)
✅ cogs/
✅ assets/
✅ web/  (BARU! Web dashboard)
```

### Step 2: Konfigurasi di Panel
```
Pterodactyl Panel → Server Settings → Startup

Startup Command:
  bash start.sh

Environment Variables:
  DISCORD_TOKEN = your_token_here
  GROQ_API_KEY = your_key (optional)
  PORT = 5000 (optional, default: 5000)
  PYTHONUNBUFFERED = 1 (recommended)

Port Allocations:
  ✅ 5000/TCP (Web Dashboard)
```

### Step 3: Allocate Resources
```
CPU:  1-2 cores
RAM:  1 GB (untuk semua features)
Disk: 2 GB
```

### Step 4: Start Bot
```
Klik tombol START di Pterodactyl Panel
```

---

## 🌐 Akses Web Dashboard

Setelah bot running:

### URL
```
http://<your-server-ip>:5000
```

### Contoh (Local):
```
http://localhost:5000
http://192.168.1.100:5000
http://my-pterodactyl.com:5000
```

### Fitur Dashboard
- ✅ Bot status real-time
- ✅ List semua commands
- ✅ Bot statistics
- ✅ Multi-language (EN/ID)

### API Endpoints
```
GET  /              → Main dashboard
GET  /api/status    → Bot online status
GET  /api/stats     → Bot statistics
GET  /api/health    → Health check
GET  /api/translations/<lang>  → Translations
```

---

## 📊 Logging System

### Log File Location
```
Pterodactyl: /home/container/bot.log
Local: discord bot tapi versi gwe/bot.log
```

### Log Format
```
TIMESTAMP | [LEVEL] | MODULE | MESSAGE

Contoh:
2024-01-15 10:30:45,123 | [INFO]    | DiscordBot | [READY] Bot connected to Discord!
2024-01-15 10:30:46,456 | [INFO]    | FlaskApp   | [WEB] Dashboard access from 192.168.1.1
2024-01-15 10:30:47,789 | [WARNING] | FlaskApp   | Flask warning message
2024-01-15 10:30:48,123 | [ERROR]   | DiscordBot | [ERROR] Connection failed: <error>
```

### View Logs in Pterodactyl
```
Method 1: Console (Live)
  Pterodactyl Panel → Console tab (real-time output)

Method 2: File Manager
  Pterodactyl Panel → File Manager → bot.log

Method 3: Via Console Command
  tail -f bot.log
  grep "\[WEB\]" bot.log
  tail -50 bot.log
```

### Log Levels
```
[INFO]    = Informational messages (bot startup, commands, etc)
[WARNING] = Warning messages (missing features, etc)
[ERROR]   = Error messages (connection failed, etc)
[DEBUG]   = Debug information (very detailed, for troubleshooting)
```

---

## ✅ Verification Checklist

Setelah bot start, verifikasi:

- [ ] Discord bot online (show in Discord server)
- [ ] Web dashboard accessible (http://localhost:5000)
- [ ] Bot responds to commands (!ping, !hello)
- [ ] Logs appear in pterodactyl console
- [ ] bot.log file is being updated
- [ ] Web requests logged with [WEB] prefix
- [ ] Port 5000 open and accessible

---

## 🧪 Testing Commands

### Test Discord Bot
```
!ping          → Check latency
!hello         → Get greeting
!info          → Bot information
```

### Test Web Server (curl)
```bash
# Health check
curl http://localhost:5000/api/health

# Bot status
curl http://localhost:5000/api/status

# Statistics
curl http://localhost:5000/api/stats

# Translations
curl http://localhost:5000/api/translations/en
curl http://localhost:5000/api/translations/id
```

### Test Logs
```bash
# View last 20 lines
tail -20 bot.log

# Monitor live (auto-update)
tail -f bot.log

# Count [WEB] logs
grep -c "\[WEB\]" bot.log

# See only web logs
grep "\[WEB\]" bot.log

# See only errors
grep "\[ERROR\]" bot.log
```

---

## 🔧 Troubleshooting

### Problem: Web server not accessible
```
Solution:
1. Check port 5000 allocated in Pterodactyl
2. Check firewall rules
3. Verify in logs: grep "[WEB] Starting" bot.log
4. Test: curl http://localhost:5000/api/health
```

### Problem: Bot starts but web server doesn't
```
Solution:
1. Check that web/ folder exists
2. Verify web/app.py is not corrupted
3. Check for Flask import errors in logs
4. Re-upload web/ folder
```

### Problem: Logs not being written
```
Solution:
1. Check file permissions: chmod 666 bot.log
2. Verify bot.py path is correct
3. Check disk space: df -h
4. Try: truncate -s 0 bot.log (clear old logs)
```

### Problem: Port 5000 already in use
```
Solution (Pterodactyl):
1. Set PORT environment variable to different port
   PORT=5001 (or any free port)
2. Access at: http://localhost:5001

Solution (Local):
   Set PORT=5001 in .env or environment
```

---

## 📝 Configuration Files Modified

| File | Changes |
|------|---------|
| `web/app.py` | Added logging, flask setup |
| `start.sh` | Added web server startup, logging |
| `PTERODACTYL_CONFIG.md` | Added port config, web docs |
| `PTERODACTYL_SETUP.md` | Added web server section |

---

## 🎯 Summary

✅ **Bot Setup**: Complete
- Discord bot dengan AI, music, moderation commands
- Logging ke console & bot.log

✅ **Web Dashboard**: Complete  
- Flask web server on port 5000
- Logging setiap request ke bot.log
- Multi-language support
- Real-time statistics

✅ **Pterodactyl Panel**: Complete
- Startup script menjalankan keduanya
- Auto-restart jika crash
- Full logging & monitoring
- Documentation lengkap

✅ **Logging System**: Complete
- Unified log file (bot.log)
- Consistent format
- Both services log dengan prefix
- Easy to monitor & debug

---

**Version**: 2.1  
**Last Updated**: March 2026  
**Status**: Production Ready ✅
