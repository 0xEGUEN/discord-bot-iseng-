import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Command: ping
@bot.command(name='ping', help='Responds with pong!')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# Command: hello
@bot.command(name='hello', help='Greet the user')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}! 👋')

# Command: echo
@bot.command(name='echo', help='Echo your message - Usage: !echo <message>')
async def echo(ctx, *, message):
    await ctx.send(message)

# Command: info
@bot.command(name='info', help='Get bot info')
async def info(ctx):
    embed = discord.Embed(title='Bot Info', color=discord.Color.blue())
    embed.add_field(name='Bot Name', value=bot.user.name, inline=False)
    embed.add_field(name='Bot ID', value=bot.user.id, inline=False)
    embed.add_field(name='Latency', value=f'{round(bot.latency * 1000)}ms', inline=False)
    await ctx.send(embed=embed)

# Command: help (override default help)
@bot.command(name='commands', help='List all available commands')
async def list_commands(ctx):
    embed = discord.Embed(title='Available Commands', color=discord.Color.green())
    for command in bot.commands:
        embed.add_field(name=f'!{command.name}', value=command.help, inline=False)
    await ctx.send(embed=embed)

# Run the bot
if __name__ == '__main__':
    bot.run(TOKEN)
