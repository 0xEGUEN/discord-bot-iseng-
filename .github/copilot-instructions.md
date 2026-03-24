# Discord Bot Project Setup

## Project Overview
Simple Discord bot built with discord.py containing 5 basic commands: ping, hello, echo, info, and commands listing.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
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
```bash
python bot.py
```

## Available Commands
- `!ping` - Check bot latency
- `!hello` - Greeting message
- `!echo <message>` - Echo user message
- `!info` - Bot information
- `!commands` - List all commands

## File Structure
- `bot.py` - Main bot application
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create from .env.example)
- `README.md` - Full documentation

## Notes
- Make sure `.env` is in `.gitignore` to protect your token
- Bot uses discord.py command framework
- Default prefix is `!`
