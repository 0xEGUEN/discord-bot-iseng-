import discord
from discord.ext import commands
from discord import app_commands
import os
from groq import Groq

class AICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Use bot's Groq client if available, otherwise create new one
        if hasattr(bot, 'groq_client') and bot.groq_client:
            self.groq_client = bot.groq_client
        else:
            groq_key = os.getenv('GROQ_API_KEY')
            if groq_key:
                try:
                    self.groq_client = Groq(api_key=groq_key)
                except Exception as e:
                    print(f'[AI_COMMANDS] Failed to initialize Groq: {e}')
                    self.groq_client = None
            else:
                self.groq_client = None

    @app_commands.command(name="ask", description="Ask AI a question")
    @app_commands.describe(question="Your question for the AI")
    async def ask(self, interaction: discord.Interaction, question: str):
        """Chat with Groq AI"""
        await interaction.response.defer()
        
        try:
            if not self.groq_client:
                await interaction.followup.send("❌ AI service not configured")
                return
            
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": question}
                ],
                max_tokens=500
            )
            
            # Validate API response
            if not response.choices or len(response.choices) == 0:
                await interaction.followup.send("❌ Empty response from AI")
                return
            
            answer = response.choices[0].message.content
            
            # Handle None response
            if not answer:
                await interaction.followup.send(f"❌ Empty response from AI")
                return
            
            # Split long responses into multiple messages if needed
            if len(answer) > 2000:
                for i in range(0, len(answer), 2000):
                    await interaction.followup.send(answer[i:i+2000])
            else:
                await interaction.followup.send(answer)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}")

    @app_commands.command(name="imagine", description="Generate creative text")
    @app_commands.describe(prompt="Creative prompt for the AI")
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        """Generate creative content"""
        await interaction.response.defer()
        
        try:
            if not self.groq_client:
                await interaction.followup.send("❌ AI service not configured")
                return
            
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": f"Create something creative based on this: {prompt}"}
                ],
                max_tokens=500
            )
            
            # Validate API response
            if not response.choices or len(response.choices) == 0:
                await interaction.followup.send("❌ Empty response from AI")
                return
            
            result = response.choices[0].message.content
            
            # Handle None response
            if not result:
                await interaction.followup.send(f"❌ Empty response from AI")
                return
            
            if len(result) > 2000:
                for i in range(0, len(result), 2000):
                    await interaction.followup.send(result[i:i+2000])
            else:
                await interaction.followup.send(result)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}")

async def setup(bot):
    await bot.add_cog(AICommands(bot))
