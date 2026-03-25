# Discord Bot Project Setup

## Project Overview
Simple Discord bot built with discord.py containing 5 basic commands: ping, hello, echo, info, and commands listing.

## Quick Start

### Choose Your Runtime:

#### Option A: Python (Original)
```bash
pip install -r requirements.txt
python bot.py
```

#### Option B: Node.js (New - Recommended)
```bash
npm install
npm start
```

#### Option C: Pterodactyl Panel (Hosting)
```bash
# Upload files to panel
# Set startup command: bash start.sh
# Set DISCORD_TOKEN in environment
# Click Start button
```

---

### 1. Install Dependencies

**Python:**
```bash
pip install -r requirements.txt
```

**Node.js:**
```bash
npm install
```

### 2. Get Discord Bot Token
1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Create New Application
3. Go to Bot tab → Add Bot
4. Copy the TOKEN

### 3. Configure Bot
1. Rename `.env.example` to `.env`
2. Paste your token: `DISCORD_TOKEN=your_token`

### 4. Invite Bot to Server
1. Developer Portal → OAuth2 → URL Generator
2. Select scope: `bot`
3. Select permissions: `Send Messages`, `Read Messages/View Channels`
4. Open generated URL and add bot to server

### 5. Run Bot

**Python:**
```bash
python bot.py
```

**Node.js (Recommended):**
```bash
npm start
```

### Node.js Additional Commands
```bash
npm run setup       # Interactive setup wizard
npm run check-env   # Verify environment
npm run dev         # Development mode
```


## Available Commands
- `!ping` - Check bot latency
- `!hello` - Greeting message
- `!echo <message>` - Echo user message
- `!info` - Bot information
- `!commands` - List all commands

## File Structure
**Core Files:**
- `bot.py` - Main bot application
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create from .env.example)
- `README.md` - Full documentation

**Node.js Wrapper Files:**
- `bot.js` - Node.js wrapper to run bot.py
- `package.json` - Node.js dependencies & scripts
- `check-env.js` - Environment verification
- `setup.js` - Interactive setup wizard
- `README_NODEJS.md` - Node.js setup guide

**Pterodactyl Panel Files:**
- `start.sh` - Pterodactyl startup script
- `Dockerfile` - Docker configuration
- `PTERODACTYL_SETUP.md` - Pterodactyl setup guide
- `PTERODACTYL_CONFIG.md` - Pterodactyl configuration
- `PTERODACTYL_STARTUP.txt` - Startup command reference


## Notes
- Make sure `.env` is in `.gitignore` to protect your token
- Bot uses discord.py command framework
- Default prefix is `!`
