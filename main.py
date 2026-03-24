import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import asyncio
import traceback

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Validate environment variables
if not TOKEN:
    print('[ERROR] DISCORD_TOKEN environment variable not set')
    print('Please create a .env file with your Discord token')
    exit(1)

# Create bot instance with slash commands support
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Load all cogs from the cogs folder
async def load_cogs():
    cogs_folder = './cogs'
    cogs_loaded = 0
    cogs_failed = 0
    
    if not os.path.exists(cogs_folder):
        print(f'[ERROR] {cogs_folder} directory not found')
        return
    
    for filename in os.listdir(cogs_folder):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'[OK] Loaded {filename}')
                cogs_loaded += 1
            except Exception as e:
                print(f'[ERROR] Failed to load {filename}: {e}')
                traceback.print_exc()
                cogs_failed += 1
    
    print(f'[INFO] Loaded {cogs_loaded} cog(s), {cogs_failed} failed')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())