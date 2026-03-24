import discord
from discord.ext import commands
from discord import app_commands
import os
from groq import Groq
import logging
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger('DiscordBot')

# Rate limiting: 5 requests per user per minute
RATE_LIMIT = 5
RATE_LIMIT_WINDOW = 60

class AICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_requests = defaultdict(list)
        
        # Use bot's Groq client if available, otherwise create new one
        if hasattr(bot, 'groq_client') and bot.groq_client:
            self.groq_client = bot.groq_client
        else:
            groq_key = os.getenv('GROQ_API_KEY')
            if groq_key:
                try:
                    self.groq_client = Groq(api_key=groq_key)
                    logger.info('[AI] Groq client initialized')
                except Exception as e:
                    logger.error(f'[AI] Failed to initialize Groq: {e}')
                    self.groq_client = None
            else:
                logger.warning('[AI] GROQ_API_KEY not set')
                self.groq_client = None

    def _check_rate_limit(self, user_id: int) -> bool:
        """Check if user exceeded rate limit"""
        now = datetime.now()
        user_key = str(user_id)
        
        # Clean old requests
        self.user_requests[user_key] = [
            t for t in self.user_requests[user_key] 
            if (now - t).total_seconds() < RATE_LIMIT_WINDOW
        ]
        
        # Check limit
        if len(self.user_requests[user_key]) >= RATE_LIMIT:
            return False
        
        self.user_requests[user_key].append(now)
        return True

    @app_commands.command(name="ask", description="Ask AI a question")
    @app_commands.describe(question="Your question for the AI")
    async def ask(self, interaction: discord.Interaction, question: str):
        """Chat with Groq AI with improved error handling"""
        await interaction.response.defer()
        
        try:
            # Rate limit check
            if not self._check_rate_limit(interaction.user.id):
                await interaction.followup.send(
                    "⏱️ You're sending too many requests. Please wait a moment.",
                    ephemeral=True
                )
                logger.warning(f'[AI] Rate limit exceeded for user {interaction.user}')
                return
            
            if not self.groq_client:
                await interaction.followup.send("❌ AI service not configured")
                logger.error('[AI] Groq client not initialized')
                return
            
            # Validate question
            if not question or len(question) > 1000:
                await interaction.followup.send("❌ Question must be between 1-1000 characters")
                return
            
            logger.info(f'[AI] Processing question from {interaction.user}: {question[:100]}...')
            
            response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": question}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
            
            # Validate API response
            if not response or not response.choices:
                await interaction.followup.send("❌ No response from AI service")
                logger.error('[AI] Empty response from Groq API')
                return
            
            answer = response.choices[0].message.content
            
            # Handle None response
            if not answer or answer.strip() == "":
                await interaction.followup.send("❌ AI returned empty response")
                logger.error('[AI] Empty message content from API')
                return
            
            logger.info(f'[AI] Got response ({len(answer)} chars)')
            
            # Split and send response (Discord has 2000 char limit)
            if len(answer) > 2000:
                logger.debug(f'[AI] Splitting response into {(len(answer) + 1999) // 2000} messages')
                for i in range(0, len(answer), 2000):
                    chunk = answer[i:i+2000]
                    await interaction.followup.send(chunk)
            else:
                await interaction.followup.send(answer)
                
        except ValueError as ve:
            logger.error(f'[AI] Validation error: {ve}')
            await interaction.followup.send(f"❌ Invalid input: {str(ve)[:100]}")
        except Exception as e:
            logger.error(f'[AI] Unexpected error: {type(e).__name__}: {str(e)}')
            await interaction.followup.send(f"❌ Error: {type(e).__name__}")

    @app_commands.command(name="imagine", description="Generate creative text")
    @app_commands.describe(prompt="Creative prompt for the AI")
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        """Generate creative content with improved error handling"""
        await interaction.response.defer()
        
        try:
            # Rate limit check
            if not self._check_rate_limit(interaction.user.id):
                await interaction.followup.send(
                    "⏱️ You're sending too many requests. Please wait a moment.",
                    ephemeral=True
                )
                logger.warning(f'[AI] Rate limit exceeded for user {interaction.user}')
                return
            
            if not self.groq_client:
                await interaction.followup.send("❌ AI service not configured")
                return
            
            # Validate prompt
            if not prompt or len(prompt) > 1000:
                await interaction.followup.send("❌ Prompt must be between 1-1000 characters")
                return
            
            logger.info(f'[AI] Generating creative content for: {prompt[:100]}...')
            
            response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Create something creative and imaginative based on this prompt. Be creative and original: {prompt}"
                        }
                    ],
                    max_tokens=500,
                    temperature=0.9  # Higher temperature for more creativity
                )
            
            # Validate API response
            if not response or not response.choices:
                await interaction.followup.send("❌ No response from AI service")
                logger.error('[AI] Empty response from Groq API')
                return
            
            result = response.choices[0].message.content
            
            # Handle None response
            if not result or result.strip() == "":
                await interaction.followup.send("❌ AI returned empty response")
                return
            
            logger.info(f'[AI] Generated {len(result)} characters')
            
            # Split and send response
            if len(result) > 2000:
                for i in range(0, len(result), 2000):
                    chunk = result[i:i+2000]
                    await interaction.followup.send(chunk)
            else:
                await interaction.followup.send(result)
                
        except Exception as e:
            logger.error(f'[AI] Imagine error: {type(e).__name__}: {str(e)}')
            await interaction.followup.send(f"❌ Error: {type(e).__name__}")

async def setup(bot):
    await bot.add_cog(AICommands(bot))
