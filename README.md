# Discord Bot Version 2.1

Advanced Discord bot dengan fitur music, AI, moderation, dan web dashboard.

**Status**: Production Ready ✅  
**Version**: 2.1  
**Python**: 3.10+

## 🎯 Fitur Utama

### 🎵 Music Player
- Play musik dari YouTube
- Loop modes (off, song, queue)
- Shuffle queue
- Save/Load playlists
- Pause, resume, skip, stop
- Show queue & now playing

### 🤖 AI Commands
- Ask AI questions (Groq LLaMA 3.3)
- Generate creative text
- Rate limiting (5/min per user)
- Better error handling
- Long response support

### 🛡️ Moderation (NEW!)
- Ban/Kick users
- Warning system (auto-kick at 3)
- Voice mute/unmute
- Audit logging (audit_log.json)
- Warn tracking (warns.json)

### 🎛️ Utility
- Ping latency
- Bot info
- Echo messages
- Multi-language support (EN/ID)
- Streaming status "build with love"

### 📊 Web Dashboard
- Real-time stats
- Command list
- Language switcher
- Bot status display

## 📦 Installation

### 1. Clone atau Download Project
```bash
git clone <repository>
cd discord-bot
```

### 2. Setup Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Discord Bot Token
1. Buka [Discord Developer Portal](https://discord.com/developers/applications)
2. Klik "New Application"
3. Pergi ke "Bot" → "Add Bot"
4. Copy token dari "TOKEN" section

### 5. Setup Environment Variables
```bash
# Copy .env.example ke .env
cp .env.example .env

# Edit .env dan tambahkan:
DISCORD_TOKEN=your_bot_token_here
GROQ_API_KEY=your_groq_key_here  # Optional
```

### 6. Configure Bot Permissions
Di [Developer Portal](https://discord.com/developers/applications):

**OAuth2 → URL Generator:**
- Scopes: `bot`, `applications.commands`
- Permissions:
  - General: `Administrator` (or specific permissions below)
  - Text: `Send Messages`, `Read Messages`
  - Voice: `Connect`, `Speak`, `Mute Members`
  - Moderation: `Ban Members`, `Kick Members`, `Manage Messages`

Copy generated URL dan invite bot ke server Anda.

### 7. Run Bot
```bash
python bot.py
```

Success message:
```
============================================================
[BOT] DISCORD BOT STARTING UP
============================================================
[READY] Bot has connected to Discord!
[STATUS] Bot status set to: Streaming "build with love"
============================================================
```

---

## 🎮 Command Examples

### 🎵 Music Commands
```
/play "Never Gonna Give You Up"   # Play song
/pause                            # Pause music
/resume                           # Resume music
/skip                             # Skip song
/stop                             # Stop & disconnect
/queue                            # Show queue
/nowplaying                       # Current song
/loop queue                       # Loop mode: off, song, queue
/shuffle                          # Shuffle queue
/saveplaylist "My Mix"            # Save playlist
/loadplaylist "My Mix"            # Load playlist
```

### 🤖 AI Commands
```
/ask "What is Python?"            # Ask AI
/imagine "A cyberpunk city"       # Generate text
```

### 🛡️ Moderation Commands
```
/ban @user Spam                   # Ban user
/kick @user Trolling              # Kick user
/warn @user Rudeness              # Warn user
/warns @user                      # Check warns
/clearwarns @user                 # Admin: clear warns
/mute @user 10                    # Mute 10 minutes
/unmute @user                     # Unmute user
```

### 🎛️ Utility Commands
```
!ping                             # Bot latency
!hello                            # Greeting
!echo hello                       # Echo message
!info                             # Bot info
!commands                         # List all commands
```

---

## 📁 Project Structure
```
discord-bot/
├── bot.py                        # Main bot entry
├── main.py                       # Alt entry point
├── requirements.txt              # Dependencies
├── .env                          # Config (create from .env.example)
├── .env.example                  # Config template
├── bot.log                       # Bot logs
├── warns.json                    # Warning storage
├── audit_log.json                # Moderation logs
├── playlists.json                # User playlists
├── cogs/
│   ├── moderation_commands.py   # Ban, kick, warn, mute
│   ├── music_commands.py        # Music player
│   ├── ai_commands.py           # AI features
│   └── utility_commands.py      # Basic commands
├── web/
│   ├── app.py                   # Flask backend
│   ├── static/
│   │   ├── style.css
│   │   └── script.js
│   └── templates/
│       └── index.html           # Dashboard
└── docs/
    └── IMPROVEMENTS_GUIDE.md    # Detailed improvements
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
DISCORD_TOKEN=your_bot_token
GROQ_API_KEY=your_groq_api_key    # Optional
BOT_PREFIX=!
LOG_LEVEL=info
```

### JSON Files
- **warns.json**: User warnings per guild
- **audit_log.json**: Moderation action logs
- **playlists.json**: User-specific playlists

---

## 🔧 Troubleshooting

### Bot tidak connect
```
❌ [INIT] DISCORD_TOKEN environment variable not set
```
**Solution**: Buat `.env` file dan tambahkan `DISCORD_TOKEN=<your_token>`

### Music tidak play
```
❌ [MUSIC] FFmpeg not installed
```
**Solution**: Install FFmpeg
- Windows: `choco install ffmpeg` atau download dari [ffmpeg.org](https://ffmpeg.org)
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### AI tidak respond
```
❌ [AI] GROQ_API_KEY not set
```
**Solution**: Dapatkan API key dari [console.groq.com](https://console.groq.com) dan tambahkan ke `.env`

### Command permission error
**Solution**: Pastikan bot memiliki permission yang cukup dan berada di atas user dalam role hierarchy.

---

## 📊 Web Dashboard

Akses dashboard di `http://localhost:5000` (jika running dengan web server)

Features:
- Real-time bot stats (latency, members, guilds)
- Interactive command list
- Language selector
- Bot status display

---

## 🔒 Security

- ✅ Token disimpan di `.env` (add to `.gitignore`)
- ✅ Rate limiting on AI commands
- ✅ Input validation
- ✅ Permission checks
- ✅ Audit logging untuk actions
- ✅ Error recovery

---

## 📝 Dokumentasi Lengkap

Untuk dokumentasi lebih detail tentang fitur baru:
- **[IMPROVEMENTS_GUIDE.md](./IMPROVEMENTS_GUIDE.md)** - Fitur dan improvements v2.1

---

## 🚀 Deployment

### Heroku
1. Create `Procfile`:
```
web: gunicorn web.app:app
bot: python bot.py
```

2. Deploy:
```bash
git push heroku main
```

### Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

### VPS/Server
```bash
# Install dependencies
apt install python3.11 ffmpeg

# Setup env
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with supervisor/systemd
python3.11 bot.py
```

---

## 📈 Stats

- **Commands**: 20+
- **Languages**: English, Indonesian
- **Database**: JSON-based
- **Response Time**: <100ms average
- **Uptime**: Production-grade

---

## 📄 License

MIT License - Feel free to use for your projects!

---

## 🤝 Contributing

Suggestions dan improvements welcome! Silakan buat issue atau pull request.

---

## 📞 Support

- Check `bot.log` untuk error details
- Lihat `audit_log.json` untuk moderation history
- Baca `IMPROVEMENTS_GUIDE.md` untuk feature docs

---

**Last Updated**: Version 2.1  
**Maintained**: 2024
