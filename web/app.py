from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import sys
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from language_support import get_language, translate

load_dotenv()

# Setup Logging for Web App
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | [%(levelname)-8s] | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('../bot.log', encoding='utf-8')
    ]
)

logger = logging.getLogger('FlaskApp')
logger.setLevel(logging.INFO)

app = Flask(__name__)

# Security: Disable debug mode in production
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['DEBUG'] = DEBUG_MODE
app.config['ENV'] = 'development' if DEBUG_MODE else 'production'

logger.info('[WEB] Flask Web Server Initializing')
logger.info(f'[WEB] Debug Mode: {DEBUG_MODE}')

# Dummy stats (in production, you'd connect to the actual bot)
bot_stats = {
    "is_online": True,
    "uptime_seconds": 3600,
    "guilds": 5,
    "users": 150,
    "latency_ms": 45,
    "version": "1.0.0",
    "commands_used": 1234,
    "music_playing": False
}

@app.route('/')
def dashboard():
    lang = request.args.get('lang', 'en')
    if lang not in ['en', 'id']:
        lang = 'en'
    
    logger.info(f'[WEB] Dashboard access from {request.remote_addr} - Language: {lang}')
    
    translations = get_language(lang)
    
    bot_name = "ChatGPT AI Bot"
    commands = [
        {
            "name": "/ping",
            "description": "Check bot latency",
            "type": "utility"
        },
        {
            "name": "/hello",
            "description": "Get a greeting from the bot",
            "type": "utility"
        },
        {
            "name": "/echo",
            "description": "Echo your message",
            "type": "utility"
        },
        {
            "name": "/info",
            "description": "Get bot information",
            "type": "utility"
        },
        {
            "name": "/ask",
            "description": "Ask AI a question",
            "type": "ai"
        },
        {
            "name": "/imagine",
            "description": "Generate creative text",
            "type": "ai"
        },
        {
            "name": "/play",
            "description": "Play music from YouTube",
            "type": "music"
        },
        {
            "name": "/skip",
            "description": "Skip to next song",
            "type": "music"
        }
    ]
    
    return render_template('index.html', 
                         bot_name=bot_name, 
                         commands=commands,
                         current_lang=lang,
                         translations=json.dumps(translations))

@app.route('/api/status')
def get_status():
    logger.info(f'[WEB] Status API request from {request.remote_addr}')
    return {
        "status": "online" if bot_stats["is_online"] else "offline",
        "bot_name": "ChatGPT AI Bot",
        "features": ["Slash Commands", "AI Chat", "Music Player", "Web Dashboard"]
    }

@app.route('/api/stats')
def get_stats():
    """Get real-time bot statistics"""
    logger.info(f'[WEB] Stats API request from {request.remote_addr}')
    def format_uptime(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    
    return jsonify({
        "online": bot_stats["is_online"],
        "uptime": format_uptime(bot_stats["uptime_seconds"]),
        "guilds": bot_stats["guilds"],
        "users": bot_stats["users"],
        "latency": f"{bot_stats['latency_ms']}ms",
        "version": bot_stats["version"],
        "commands_used": bot_stats["commands_used"],
        "music_playing": bot_stats["music_playing"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/translations/<lang>')
def get_translations(lang):
    """Get translations for a specific language"""
    logger.info(f'[WEB] Translations request from {request.remote_addr} - Language: {lang}')
    # Input validation: prevent injection attacks
    if not isinstance(lang, str) or len(lang) > 5 or not lang.isalpha():
        lang = 'en'
    if lang not in ['en', 'id']:
        lang = 'en'
    return jsonify(get_language(lang))

@app.route('/api/health')
def health_check():
    """Quick health check"""
    logger.info(f'[WEB] Health check from {request.remote_addr}')
    return jsonify({
        "healthy": True,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Use environment variable for debug mode
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')  # Default to localhost, can override with 0.0.0.0
    logger.info('=' * 60)
    logger.info(f'[WEB] Starting Flask Web Server')
    logger.info(f'[WEB] Host: {host} | Port: {port}')
    logger.info(f'[WEB] Debug Mode: {DEBUG_MODE}')
    logger.info('=' * 60)
    app.run(debug=DEBUG_MODE, port=port, host=host)
