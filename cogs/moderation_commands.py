import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime, timedelta
import logging
import asyncio

logger = logging.getLogger('DiscordBot')

# File to store warns
WARNS_FILE = 'warns.json'
AUDIT_LOG_FILE = 'audit_log.json'

def load_warns():
    """Load warns from file"""
    if os.path.exists(WARNS_FILE):
        try:
            with open(WARNS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_warns(warns):
    """Save warns to file"""
    with open(WARNS_FILE, 'w') as f:
        json.dump(warns, f, indent=2)

def log_audit(action, target, moderator, reason=""):
    """Log moderation action to audit log"""
    try:
        audit_log = []
        if os.path.exists(AUDIT_LOG_FILE):
            with open(AUDIT_LOG_FILE, 'r') as f:
                audit_log = json.load(f)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'target': str(target),
            'target_id': target.id if hasattr(target, 'id') else '',
            'moderator': str(moderator),
            'moderator_id': moderator.id,
            'reason': reason
        }
        audit_log.append(log_entry)
        
        # Keep only last 1000 entries
        if len(audit_log) > 1000:
            audit_log = audit_log[-1000:]
        
        with open(AUDIT_LOG_FILE, 'w') as f:
            json.dump(audit_log, f, indent=2)
        
        logger.info(f'[AUDIT] {action}: {target} by {moderator} - {reason}')
    except Exception as e:
        logger.error(f'[AUDIT] Error logging action: {e}')

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = load_warns()
        self.muted_users = set()

    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.describe(
        user="User to ban",
        reason="Reason for ban"
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided"):
        """Ban a user"""
        try:
            if not interaction.guild:  # type: ignore
                await interaction.response.send_message("❌ This command only works in servers!", ephemeral=True)
                return
            await interaction.guild.ban(user, reason=reason)  # type: ignore
            log_audit('BAN', user, interaction.user, reason)
            
            embed = discord.Embed(
                title="🚫 User Banned",
                description=f"**{user}** has been banned",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="By", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            logger.info(f'[MOD] {user} banned by {interaction.user} - {reason}')
        except Exception as e:
            logger.error(f'[MOD] Ban error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.describe(
        user="User to kick",
        reason="Reason for kick"
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided"):
        """Kick a user"""
        try:
            if not interaction.guild:  # type: ignore
                await interaction.response.send_message("❌ This command only works in servers!", ephemeral=True)
                return
            await interaction.guild.kick(user, reason=reason)  # type: ignore
            log_audit('KICK', user, interaction.user, reason)
            
            embed = discord.Embed(
                title="👢 User Kicked",
                description=f"**{user}** has been kicked",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="By", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            logger.info(f'[MOD] {user} kicked by {interaction.user} - {reason}')
        except Exception as e:
            logger.error(f'[MOD] Kick error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.describe(
        user="User to warn",
        reason="Reason for warning"
    )
    @commands.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided"):
        """Warn a user"""
        try:
            if not interaction.guild:  # type: ignore
                await interaction.response.send_message("❌ This command only works in servers!", ephemeral=True)
                return
            user_id = str(user.id)
            guild_id = str(interaction.guild.id)  # type: ignore
            
            if guild_id not in self.warns:
                self.warns[guild_id] = {}
            if user_id not in self.warns[guild_id]:
                self.warns[guild_id][user_id] = []
            
            self.warns[guild_id][user_id].append({
                'reason': reason,
                'date': datetime.now().isoformat(),
                'by': str(interaction.user)
            })
            
            save_warns(self.warns)
            log_audit('WARN', user, interaction.user, reason)
            
            warn_count = len(self.warns[guild_id][user_id])
            
            embed = discord.Embed(
                title="⚠️ User Warned",
                description=f"**{user}** has been warned",
                color=discord.Color.yellow()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Total Warns", value=f"{warn_count}", inline=True)
            embed.add_field(name="By", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            logger.info(f'[MOD] {user} warned ({warn_count}) by {interaction.user} - {reason}')
            
            # Auto-kick after 3 warns
            if warn_count >= 3:
                await interaction.guild.kick(user, reason=f"Automatic kick after 3 warns")  # type: ignore
                await interaction.followup.send(f"⚠️ {user} has been automatically kicked after 3 warnings")
                log_audit('AUTO_KICK', user, self.bot.user, "3 warns threshold")
                
        except Exception as e:
            logger.error(f'[MOD] Warn error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="mute", description="Mute a user in voice")
    @app_commands.describe(
        user="User to mute",
        duration="Duration in minutes (0 for permanent)"
    )
    @commands.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, user: discord.Member, duration: int = 0):
        """Mute a user in voice"""
        try:
            if not interaction.guild:  # type: ignore
                await interaction.response.send_message("❌ This command only works in servers!", ephemeral=True)
                return
            if not user.voice or not user.voice.channel:
                await interaction.response.send_message("❌ User is not in a voice channel!", ephemeral=True)
                return
            
            await user.edit(mute=True)
            self.muted_users.add(user.id)
            
            log_audit('MUTE', user, interaction.user, f"Duration: {duration} minutes")
            
            embed = discord.Embed(
                title="🔇 User Muted",
                description=f"**{user}** has been muted",
                color=discord.Color.blue()
            )
            if duration > 0:
                embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
            
            await interaction.response.send_message(embed=embed)
            logger.info(f'[MOD] {user} muted by {interaction.user}')
            
            # Auto-unmute after duration
            if duration > 0:
                await asyncio.sleep(duration * 60)
                try:
                    member = await interaction.guild.fetch_member(user.id)  # type: ignore
                    await member.edit(mute=False)
                    self.muted_users.discard(user.id)
                    logger.info(f'[MOD] {user} auto-unmuted after {duration} minutes')
                except:
                    pass
                    
        except Exception as e:
            logger.error(f'[MOD] Mute error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="unmute", description="Unmute a user in voice")
    @app_commands.describe(user="User to unmute")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, user: discord.Member):
        """Unmute a user"""
        try:
            await user.edit(mute=False)
            self.muted_users.discard(user.id)
            
            log_audit('UNMUTE', user, interaction.user, "")
            
            embed = discord.Embed(
                title="🔊 User Unmuted",
                description=f"**{user}** has been unmuted",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed)
            logger.info(f'[MOD] {user} unmuted by {interaction.user}')
        except Exception as e:
            logger.error(f'[MOD] Unmute error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="warns", description="Check warnings for a user")
    @app_commands.describe(user="User to check")
    async def check_warns(self, interaction: discord.Interaction, user: discord.User = None):  # type: ignore
        """Check warns for a user"""
        try:
            if not interaction.guild:  # type: ignore
                await interaction.response.send_message("❌ This command only works in servers!", ephemeral=True)
                return
            target_user = user or interaction.user
            user_id = str(target_user.id)
            guild_id = str(interaction.guild.id)  # type: ignore
            
            embed = discord.Embed(
                title=f"⚠️ Warnings for {target_user}",
                color=discord.Color.yellow()
            )
            
            if guild_id in self.warns and user_id in self.warns[guild_id]:
                warns = self.warns[guild_id][user_id]
                embed.add_field(name="Total Warns", value=str(len(warns)), inline=False)
                
                for i, warn in enumerate(warns[-5:], 1):  # Show last 5
                    warn_text = f"**{warn['reason']}** (by {warn['by']})\n{warn['date']}"
                    embed.add_field(name=f"Warn #{len(warns)-5+i}", value=warn_text, inline=False)
                
                if len(warns) > 5:
                    embed.add_field(name="", value=f"... and {len(warns)-5} more", inline=False)
            else:
                embed.add_field(name="Status", value="✅ No warnings", inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f'[MOD] Warns check error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="clearwarns", description="Clear warnings for a user")
    @app_commands.describe(user="User to clear warns for")
    @commands.has_permissions(administrator=True)
    async def clear_warns(self, interaction: discord.Interaction, user: discord.User):
        """Clear all warns for a user"""
        try:
            if not interaction.guild:  # type: ignore
                await interaction.response.send_message("❌ This command only works in servers!", ephemeral=True)
                return
            user_id = str(user.id)
            guild_id = str(interaction.guild.id)  # type: ignore
            
            if guild_id in self.warns and user_id in self.warns[guild_id]:
                del self.warns[guild_id][user_id]
                save_warns(self.warns)
                
                log_audit('CLEARWARNS', user, interaction.user, "")
                
                embed = discord.Embed(
                    title="✅ Warns Cleared",
                    description=f"Warnings for **{user}** have been cleared",
                    color=discord.Color.green()
                )
                
                await interaction.response.send_message(embed=embed)
                logger.info(f'[MOD] Warns cleared for {user} by {interaction.user}')
            else:
                await interaction.response.send_message("❌ User has no warnings!", ephemeral=True)
        except Exception as e:
            logger.error(f'[MOD] Clear warns error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))
