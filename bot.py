import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from groq import Groq
import logging
import time
from datetime import datetime
import traceback
import sys

# Fix for Windows Unicode encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Setup Logging with detailed output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | [%(levelname)-8s] | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Console output with UTF-8
        logging.FileHandler('bot.log', encoding='utf-8')  # File output
    ]
)

logger = logging.getLogger('DiscordBot')
logger.setLevel(logging.DEBUG)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

logger.info('=' * 60)
logger.info('[BOT] DISCORD BOT STARTING UP')
logger.info('=' * 60)

# Initialize Groq client
try:
    client = Groq(api_key=GROQ_API_KEY)
    logger.info('[INIT] Groq client initialized')
except Exception as e:
    logger.error(f'[INIT] Failed to initialize Groq client: {e}')
    client = None

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    logger.info('=' * 60)
    logger.info(f'[READY] {bot.user} has connected to Discord!')
    logger.info(f'[READY] Bot ID: {bot.user.id}')
    logger.info(f'[READY] Latency: {round(bot.latency * 1000)}ms')
    logger.info('=' * 60)
    
    try:
        synced = await bot.tree.sync()
        logger.info(f'[SYNC] Synced {len(synced)} command(s)')
    except Exception as e:
        logger.error(f'[SYNC] Failed to sync commands: {e}')
        logger.debug(traceback.format_exc())

# Global error handler
@bot.event
async def on_command_error(ctx, error):
    logger.error(f'[ERROR] Command Error in "{ctx.command}": {type(error).__name__}')
    logger.error(f'[ERROR] User: {ctx.author} | Channel: {ctx.channel}')
    logger.debug(f'[ERROR] Full error: {str(error)}')
    logger.debug(traceback.format_exc())
    
    await ctx.send(f'[ERROR] {str(error)[:100]}')

# Command: ping
@bot.command(name='ping', help='Responds with pong!')
async def ping(ctx):
    start = time.time()
    logger.info(f'[PING] Command executed by {ctx.author}')
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! {latency}ms')
    duration = round((time.time() - start) * 1000)
    logger.info(f'[PING] Completed in {duration}ms')

# Command: hello
@bot.command(name='hello', help='Greet the user')
async def hello(ctx):
    logger.info(f'[HELLO] Command executed by {ctx.author}')
    await ctx.send(f'Hello {ctx.author.name}! =^')
    logger.info(f'[HELLO] Completed successfully')

# Command: echo
@bot.command(name='echo', help='Echo your message - Usage: !echo <message>')
async def echo(ctx, *, message):
    logger.info(f'[ECHO] Command executed by {ctx.author}')
    logger.info(f'[ECHO] Message: {message[:100]}...' if len(message) > 100 else f'[ECHO] Message: {message}')
    await ctx.send(message)
    logger.info(f'[ECHO] Completed successfully')

# Command: info
@bot.command(name='info', help='Get bot info')
async def info(ctx):
    logger.info(f'[INFO] Command executed by {ctx.author}')
    try:
        embed = discord.Embed(title='Bot Info', color=discord.Color.blue())

        embed.add_field(name='Bot Name', value=bot.user.name, inline=False)
        embed.add_field(name='Bot ID', value=bot.user.id, inline=False)
        embed.add_field(name='Latency', value=f'{round(bot.latency * 1000)}ms', inline=False)
        embed.add_field(name='Status', value='O Online', inline=False)
        await ctx.send(embed=embed)
        logger.info(f'[INFO] Completed successfully')
    except Exception as e:
        logger.error(f'[INFO] Error: {e}')
        logger.debug(traceback.format_exc())
        await ctx.send(f'[ERROR] {str(e)}')

# Command: ask (AI Chat with GPT)
@bot.command(name='ask', help='Ask AI - Usage: !ask <your question>')
async def ask(ctx, *, question):
    logger.info(f'[ASK] Command executed by {ctx.author}')
    logger.info(f'[ASK] Question: {question[:100]}...' if len(question) > 100 else f'[ASK] Question: {question}')
    
    if not client:
        logger.error('[ASK] OpenAI client not initialized')
        await ctx.send('[ERROR] AI service not available')
        return
    
    async with ctx.typing():
        start = time.time()
        try:
            logger.debug('[ASK] Calling Groq API...')
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "user", "content": question}
                ],
                max_tokens=500
            )
            answer = response.choices[0].message.content
            logger.info(f'[ASK] Got response ({len(answer)} chars)')
            
            # Split long responses into multiple messages if needed
            if len(answer) > 2000:
                logger.info(f'[ASK] Response too long, splitting into {(len(answer) + 1999) // 2000} messages')
                for i in range(0, len(answer), 2000):
                    await ctx.send(answer[i:i+2000])
            else:
                await ctx.send(answer)
            
            duration = round((time.time() - start) * 1000)
            logger.info(f'[ASK] Completed successfully in {duration}ms')
        except Exception as e:
            logger.error(f'[ASK] Error: {type(e).__name__}: {str(e)}')
            logger.debug(traceback.format_exc())
            await ctx.send(f"[ERROR] API Error: {str(e)[:100]}")

# Command: help (override default help)
@bot.command(name='commands', help='List all available commands')
async def list_commands(ctx):
    logger.info(f'[COMMANDS] Command executed by {ctx.author}')
    try:
        embed = discord.Embed(title='Available Commands', color=discord.Color.green())
        for command in bot.commands:
            embed.add_field(name=f'!{command.name}', value=command.help, inline=False)
        await ctx.send(embed=embed)
        logger.info(f'[COMMANDS] Listed {len(bot.commands)} commands')
    except Exception as e:
        logger.error(f'[COMMANDS] Error: {e}')
        logger.debug(traceback.format_exc())

# Command: sync (sync commands with Discord)
@bot.command(name='sync', help='Sync commands with Discord (Admin only)')
@commands.is_owner()
async def sync(ctx):
    logger.info(f'[SYNC] Command executed by {ctx.author}')
    try:
        logger.info('[SYNC] Syncing command tree...')
        synced = await bot.tree.sync()
        logger.info(f'[SYNC] Successfully synced {len(synced)} command(s)')
        await ctx.send(f'[OK] Synced {len(synced)} command(s)')
    except Exception as e:
        logger.error(f'[SYNC] Error: {e}')
        logger.debug(traceback.format_exc())
        await ctx.send(f'[ERROR] Failed to sync: {str(e)}')

# Run the bot
if __name__ == '__main__':
    try:
        logger.info('=' * 60)
        logger.info('[RUN] BOT STARTING...')
        logger.info('=' * 60)
        bot.run(TOKEN)
    except KeyboardInterrupt:
        logger.warning('[SHUTDOWN] Bot interrupted by user (Ctrl+C)')
    except discord.errors.LoginFailure:
        logger.error('[ERROR] Invalid Discord token!')
    except Exception as e:
        logger.error(f'[FATAL] {type(e).__name__}: {str(e)}')
        logger.debug(traceback.format_exc())
    finally:
        logger.info('=' * 60)
        logger.info('[SHUTDOWN] BOT SHUTDOWN COMPLETE')
        logger.info('=' * 60)
