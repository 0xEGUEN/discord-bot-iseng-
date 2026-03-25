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
logger.setLevel(logging.INFO)  # Enable logging

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Validate required environment variables
if not TOKEN:
    logger.error('[INIT] DISCORD_TOKEN environment variable not set')
    exit(1)

logger.info('=' * 60)
logger.info('[BOT] DISCORD BOT STARTING UP')
logger.info('=' * 60)

# Initialize Groq client
if not GROQ_API_KEY:
    logger.warning('[INIT] GROQ_API_KEY not set, AI features disabled')
    client = None
else:
    try:
        client = Groq(api_key=GROQ_API_KEY)
        logger.info('[INIT] Groq client initialized')
    except Exception as e:
        logger.error(f'[INIT] Failed to initialize Groq client: {e}')
        client = None

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Store Groq client on bot for sharing with cogs
bot.__dict__['groq_client'] = client  # type: ignore

# Event: Bot is ready
@bot.event
async def on_ready():
    logger.info('=' * 60)
    if bot.user:
        logger.info(f'[READY] {bot.user} has connected to Discord!')
        logger.info(f'[READY] Bot ID: {bot.user.id}')
    else:
        logger.warning('[READY] bot.user is None')
    logger.info(f'[READY] Latency: {round(bot.latency * 1000)}ms')
    logger.info('=' * 60)
    
    # Set bot status to streaming
    try:
        await bot.change_presence(activity=discord.Streaming(name='build with love', url='https://twitch.tv/'))
        logger.info('[STATUS] Bot status set to: Streaming "build with love"')
    except Exception as e:
        logger.error(f'[STATUS] Failed to set bot status: {e}')
    
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

        if bot.user:
            embed.add_field(name='Bot Name', value=bot.user.name, inline=False)
            embed.add_field(name='Bot ID', value=bot.user.id, inline=False)
        else:
            embed.add_field(name='Bot Status', value='Not ready yet', inline=False)
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
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": question}
                ],
                max_tokens=500
            )
            
            # Validate API response
            if not response.choices or len(response.choices) == 0:
                logger.error('[ASK] Empty response from API')
                await ctx.send('❌ Empty response from AI')
                return
            
            answer = response.choices[0].message.content
            
            # Handle None response
            if not answer:
                await ctx.send("❌ Empty response from AI")
                return
            
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
@bot.command(name='help', help='List all available commands')
async def list_commands(ctx):
    logger.info(f'[HELP] Command executed by {ctx.author}')
    try:
        # Send banner first at the top
        banner_path = os.path.join(os.path.dirname(__file__), 'assets/banner.jpg')
        if os.path.exists(banner_path):
            try:
                banner_file = discord.File(banner_path, filename='banner.jpg')
                banner_embed = discord.Embed(color=discord.Color.blurple())
                banner_embed.set_image(url='attachment://banner.jpg')
                await ctx.send(file=banner_file, embed=banner_embed)
            except Exception as e:
                logger.warning(f'[HELP] Error sending banner: {e}')
        
        embeds = []
        
        # EMBED 1: MAIN + UTILITY + MUSIC
        embed1 = discord.Embed(
            title='🤖 Bot Commands (Page 1/3)',
            description='Use `/command_name` for slash commands or `!command_name` for prefix commands',
            color=discord.Color.blurple()
        )
        
        embed1.set_thumbnail(url=bot.user.avatar.url if bot.user and bot.user.avatar else '')
        
        # UTILITY COMMANDS
        embed1.add_field(
            name='🛠️ Utility Commands',
            value='Basic bot utilities',
            inline=False
        )
        utility_cmds = [
            ('🏓 `ping`', 'Check bot latency'),
            ('👋 `hello`', 'Greeting from bot'),
            ('🔊 `echo <msg>`', 'Repeat your message'),
            ('ℹ️ `info`', 'Bot information'),
        ]
        for cmd, desc in utility_cmds:
            embed1.add_field(name=cmd, value=desc, inline=False)
        
        # MUSIC COMMANDS (Part 1)
        embed1.add_field(
            name='🎵 Music Commands - Part 1',
            value='YouTube music player',
            inline=False
        )
        music_cmds_1 = [
            ('▶️ `/play <query>`', 'Play from YouTube'),
            ('⏸️ `/pause`', 'Pause music'),
            ('▶️ `/resume`', 'Resume music'),
            ('⏹️ `/stop`', 'Stop & disconnect'),
            ('⏭️ `/skip`', 'Skip song'),
        ]
        for cmd, desc in music_cmds_1:
            embed1.add_field(name=cmd, value=desc, inline=False)
        
        embeds.append(embed1)
        
        # EMBED 2: MUSIC (part 2) + AI + MODERATION (part 1)
        embed2 = discord.Embed(
            title='🤖 Bot Commands (Page 2/3)',
            color=discord.Color.blurple()
        )
        
        # MUSIC COMMANDS (Part 2)
        embed2.add_field(
            name='🎵 Music Commands - Part 2',
            value='More music features',
            inline=False
        )
        music_cmds_2 = [
            ('📋 `/queue`', 'Show queue'),
            ('🎶 `/nowplaying`', 'Current song'),
            ('🔂 `/loop`', 'Loop modes'),
            ('🔀 `/shuffle`', 'Shuffle queue'),
            ('💾 `/saveplaylist`', 'Save queue'),
            ('📂 `/loadplaylist`', 'Load playlist'),
        ]
        for cmd, desc in music_cmds_2:
            embed2.add_field(name=cmd, value=desc, inline=False)
        
        embeds.append(embed2)
        
        # EMBED 3: AI + MODERATION + ADMIN
        embed3 = discord.Embed(
            title='🤖 Bot Commands (Page 3/3)',
            color=discord.Color.blurple()
        )
        
        # AI COMMANDS
        embed3.add_field(
            name='🤖 AI Commands',
            value='Powered by Groq LLaMA 3.3',
            inline=False
        )
        ai_cmds = [
            ('💬 `/ask`', 'Ask a question'),
            ('✨ `/imagine`', 'Create text'),
        ]
        for cmd, desc in ai_cmds:
            embed3.add_field(name=cmd, value=desc, inline=False)
        
        # MODERATION COMMANDS
        embed3.add_field(
            name='🛡️ Moderation Commands',
            value='Server moderation',
            inline=False
        )
        mod_cmds = [
            ('🚫 `/ban`', 'Ban user'),
            ('👢 `/kick`', 'Kick user'),
            ('⚠️ `/warn`', 'Warn user'),
            ('🔇 `/mute`', 'Mute user'),
            ('🔊 `/unmute`', 'Unmute user'),
            ('📋 `/warns`', 'Check warns'),
            ('✅ `/clearwarns`', 'Clear warns'),
        ]
        for cmd, desc in mod_cmds:
            embed3.add_field(name=cmd, value=desc, inline=False)
        
        # ADMIN COMMANDS
        embed3.add_field(
            name='⚙️ Admin',
            value='⚡ `sync` - Sync slash commands',
            inline=False
        )
        
        # FOOTER
        embed3.set_footer(text=f'Bot v2.1 | Requested by {ctx.author}', icon_url=ctx.author.avatar.url if ctx.author.avatar else '')
        embed3.timestamp = datetime.now()
        
        embeds.append(embed3)
        
        # Send command embeds (banner already sent at top)
        try:
            await ctx.send(embeds=embeds)
        except Exception as e:
            logger.warning(f'[HELP] Error sending embeds: {e}')
            await ctx.send(embeds=embeds)
            
        logger.info(f'[HELP] Help menu displayed for {ctx.author}')
    except Exception as e:
        logger.error(f'[HELP] Error: {e}')
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

# Load cogs
async def load_cogs():
    cogs_folder = './cogs'
    cogs_loaded = 0
    cogs_failed = 0
    
    if not os.path.exists(cogs_folder):
        logger.warning(f'[COGS] {cogs_folder} directory not found')
        return
    
    for filename in os.listdir(cogs_folder):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'[COGS] Loaded {filename}')
                cogs_loaded += 1
            except Exception as e:
                logger.error(f'[COGS] Failed to load {filename}: {e}')
                logger.debug(traceback.format_exc())
                cogs_failed += 1
    
    logger.info(f'[COGS] Loaded {cogs_loaded} cog(s), {cogs_failed} failed')

@bot.event
async def setup_hook():
    await load_cogs()

# Run the bot
if __name__ == '__main__':
    try:
        logger.info('=' * 60)
        logger.info('[RUN] BOT STARTING...')
        logger.info('=' * 60)
        if not TOKEN:
            logger.error('[RUN] DISCORD_TOKEN not set in .env file')
            exit(1)
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
