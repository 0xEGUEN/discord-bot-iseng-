# Discord Bot with Slash Commands & Web Dashboard

## 📋 Project Structure
```
.
├── main.py                 # Main bot entry point
├── cogs/
│   ├── utility_commands.py # Basic commands (ping, hello, echo, info)
│   └── ai_commands.py      # AI commands (ask, imagine)
├── web/
│   ├── app.py             # Flask web server
│   ├── templates/
│   │   └── index.html     # Dashboard HTML
│   └── static/
│       ├── style.css      # Dashboard styling
│       └── script.js      # Dashboard functionality
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
Edit `.env`:
```
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
```

### 3. Run Bot
```bash
python main.py
```

### 4. Run Web Dashboard (Optional)
```bash
cd web
python app.py
```
Then open: http://localhost:5000

## ⚡ Available Slash Commands

### Utility Commands
- `/ping` - Check bot latency
- `/hello` - Get a greeting
- `/echo <message>` - Echo your message
- `/info` - Get bot information

### AI Commands
- `/ask <question>` - Chat with GPT-3.5
- `/imagine <prompt>` - Generate creative content

## 🔧 File Organization

**main.py**: Entry point that loads all cogs
**cogs/utility_commands.py**: All basic bot commands
**cogs/ai_commands.py**: AI/OpenAI integration
**web/app.py**: Flask web server
**web/templates/index.html**: Interactive dashboard
**web/static/style.css + script.js**: Dashboard styling & JavaScript

## 📝 Notes
- Slash commands are modern Discord commands (use `/` prefix)
- Web dashboard shows all available commands
- Each feature is modular in separate files
- Easy to add more commands by creating new cog files
