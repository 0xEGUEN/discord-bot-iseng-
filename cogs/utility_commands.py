import discord
from discord.ext import commands
from discord import app_commands

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        """Responds with pong and bot latency"""
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms')

    @app_commands.command(name="hello", description="Get a greeting from the bot")
    async def hello(self, interaction: discord.Interaction):
        """Greet the user"""
        await interaction.response.send_message(f'Hello {interaction.user.name}! 👋')

    @app_commands.command(name="echo", description="Echo your message")
    @app_commands.describe(message="The message to echo")
    async def echo(self, interaction: discord.Interaction, message: str):
        """Echo user message"""
        # Validate message length (Discord limit is 2000)
        if len(message) > 2000:
            await interaction.response.send_message("❌ Message is too long (max 2000 characters)")
            return
        await interaction.response.send_message(message)

    @app_commands.command(name="info", description="Get bot information")
    async def info(self, interaction: discord.Interaction):
        """Get bot info"""
        embed = discord.Embed(title='Bot Info', color=discord.Color.blue())
        embed.add_field(name='Bot Name', value=self.bot.user.name, inline=False)
        embed.add_field(name='Bot ID', value=self.bot.user.id, inline=False)
        embed.add_field(name='Latency', value=f'{round(self.bot.latency * 1000)}ms', inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
