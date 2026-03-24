import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp  # type: ignore
import asyncio
from collections import deque
import logging
import json
import os
import random
from datetime import datetime

logger = logging.getLogger('DiscordBot')

# FFmpeg options for yt-dlp
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'ytsearch',
    'quiet': True,
    'no_warnings': True,
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)  # type: ignore

# Playlists storage
PLAYLISTS_FILE = 'playlists.json'

def load_playlists():
    """Load playlists from file"""
    if os.path.exists(PLAYLISTS_FILE):
        try:
            with open(PLAYLISTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_playlists(playlists):
    """Save playlists to file"""
    with open(PLAYLISTS_FILE, 'w') as f:
        json.dump(playlists, f, indent=2)


class Song:
    """Represents a song in the queue"""
    def __init__(self, title, url, duration):
        self.title = title
        self.url = url
        self.duration = duration


class MusicPlayer:
    """Manages music playback for a guild"""
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        self.queue = deque()
        self.current = None
        self.voice_client = None
        self.is_playing = False
        self.is_paused = False
        self.loop_mode = "off"  # off, song, queue
        self.volume = 1.0

    async def play_next(self):
        """Play next song in queue"""
        if self.queue:
            self.current = self.queue.popleft()
            assert self.current is not None, "Music item should not be None"
            try:
                # Extract audio stream URL
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(self.current.url, download=False))  # type: ignore
                
                if data and 'url' in data:
                    try:
                        audio_source = discord.FFmpegPCMAudio(data['url'], **ffmpeg_options)  # type: ignore
                    except FileNotFoundError:
                        logger.error('[MUSIC] FFmpeg not installed')
                        await self.play_next()  # Try next song
                        return
                    except Exception as e:
                        logger.error(f'[MUSIC] FFmpeg error: {e}')
                        await self.play_next()  # Try next song
                        return
                    
                    def after_play(error):
                        if error:
                            logger.error(f'[MUSIC] Playback error: {error}')
                        try:
                            asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop)
                        except RuntimeError:
                            logger.error('[MUSIC] Event loop closed')
                    
                    if self.voice_client and self.voice_client.is_connected():
                        self.voice_client.play(audio_source, after=after_play)
                        self.is_playing = True
                        self.is_paused = False
                        logger.info(f'[MUSIC] Now playing: {self.current.title}')
            except Exception as e:
                logger.error(f'[MUSIC] Error playing song: {e}')
                await self.play_next()
        else:
            self.is_playing = False
            self.current = None

    async def search_song(self, query):
        """Search for song on YouTube"""
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
            
            if data and 'entries' in data:
                # Get first result
                result = data['entries'][0]
                song = Song(
                    title=result.get('title', 'Unknown'),
                    url=result.get('webpage_url', ''),
                    duration=result.get('duration', 0)
                )
                return song
            return None
        except Exception as e:
            logger.error(f'[MUSIC] Search error: {e}')
            return None


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}  # guild_id -> MusicPlayer
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Clean up player when bot leaves guild"""
        if guild.id in self.players:
            del self.players[guild.id]
            logger.info(f'[MUSIC] Cleaned up player for guild {guild.id}')

    def get_player(self, guild_id):
        """Get or create music player for guild"""
        if guild_id not in self.players:
            self.players[guild_id] = MusicPlayer(self.bot, guild_id)
        return self.players[guild_id]

    @app_commands.command(name="play", description="Play music from YouTube")
    @app_commands.describe(query="Song name or YouTube URL")
    async def play(self, interaction: discord.Interaction, query: str):
        """Play music from YouTube"""
        await interaction.response.defer()
        
        # Validate guild context
        if not interaction.guild_id:
            await interaction.followup.send("❌ This command only works in servers!")
            return
        
        # Check if user is in voice channel
        if not hasattr(interaction.user, 'voice') or not interaction.user.voice or not interaction.user.voice.channel:  # type: ignore
            await interaction.response.send_message("❌ You need to be in a voice channel first!")
            return

        voice_channel = interaction.user.voice.channel  # type: ignore
        
        try:
            player = self.get_player(interaction.guild_id)
            
            # Connect to voice if not already connected
            if not player.voice_client or not player.voice_client.is_connected():
                try:
                    player.voice_client = await voice_channel.connect()
                    # Verify connection succeeded
                    if not player.voice_client or not player.voice_client.is_connected():
                        await interaction.followup.send("❌ Failed to connect to voice channel")
                        return
                    logger.info(f'[MUSIC] Connected to {voice_channel.name}')
                except Exception as e:
                    logger.error(f'[MUSIC] Failed to connect to voice: {e}')
                    await interaction.followup.send(f"❌ Failed to connect to voice channel: {str(e)[:50]}")
                    return
            
            # Search for song
            await interaction.followup.send(f"🔍 Searching for: `{query}`...")
            song = await player.search_song(query)
            
            if not song:
                await interaction.followup.send("❌ No results found!")
                return
            
            # Add to queue
            player.queue.append(song)
            await interaction.followup.send(f"✅ Added to queue: **{song.title}**")
            
            logger.info(f'[MUSIC] Song added: {song.title}')
            
            # Play if nothing is playing
            if not player.is_playing:
                await player.play_next()
                
        except Exception as e:
            logger.error(f'[MUSIC] Play error: {e}')
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="pause", description="Pause current music")
    async def pause(self, interaction: discord.Interaction):
        """Pause music"""
        try:
            player = self.get_player(interaction.guild_id)
            
            if player.voice_client and player.voice_client.is_playing():
                player.voice_client.pause()
                player.is_paused = True
                await interaction.response.send_message("⏸️ Music paused")
                logger.info('[MUSIC] Music paused')
            else:
                await interaction.response.send_message("❌ Nothing is playing!")
        except Exception as e:
            logger.error(f'[MUSIC] Pause error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="resume", description="Resume paused music")
    async def resume(self, interaction: discord.Interaction):
        """Resume music"""
        try:
            player = self.get_player(interaction.guild_id)
            
            if player.voice_client and player.is_paused:
                player.voice_client.resume()
                player.is_paused = False
                await interaction.response.send_message("▶️ Music resumed")
                logger.info('[MUSIC] Music resumed')
            else:
                await interaction.response.send_message("❌ Nothing to resume!")
        except Exception as e:
            logger.error(f'[MUSIC] Resume error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="stop", description="Stop music and disconnect")
    async def stop(self, interaction: discord.Interaction):
        """Stop music and disconnect"""
        try:
            player = self.get_player(interaction.guild_id)
            
            if player.voice_client and player.voice_client.is_connected():
                player.voice_client.stop()
                await player.voice_client.disconnect()
                player.queue.clear()
                player.current = None
                player.is_playing = False
                await interaction.response.send_message("⏹️ Music stopped and disconnected")
                logger.info('[MUSIC] Music stopped')
            else:
                await interaction.response.send_message("❌ Bot is not connected to a voice channel!")
        except Exception as e:
            logger.error(f'[MUSIC] Stop error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="skip", description="Skip to next song")
    async def skip(self, interaction: discord.Interaction):
        """Skip current song"""
        try:
            player = self.get_player(interaction.guild_id)
            
            if player.voice_client and player.voice_client.is_playing():
                player.voice_client.stop()
                await interaction.response.send_message("⏭️ Skipped to next song")
                logger.info('[MUSIC] Song skipped')
            else:
                await interaction.response.send_message("❌ Nothing is playing!")
        except Exception as e:
            logger.error(f'[MUSIC] Skip error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="queue", description="Show music queue")
    async def queue(self, interaction: discord.Interaction):
        """Show queue"""
        try:
            player = self.get_player(interaction.guild_id)
            
            embed = discord.Embed(title="🎵 Music Queue", color=discord.Color.purple())
            
            if player.current:
                embed.add_field(name="Now Playing", value=f"**{player.current.title}**", inline=False)
            
            if player.queue:
                queue_list = "\n".join([f"{i+1}. {song.title}" for i, song in enumerate(list(player.queue)[:10])])
                embed.add_field(name="Queue", value=queue_list, inline=False)
                
                if len(player.queue) > 10:
                    embed.add_field(name="More", value=f"...and {len(player.queue) - 10} more songs", inline=False)
            else:
                embed.add_field(name="Queue", value="Queue is empty", inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f'[MUSIC] Queue error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="nowplaying", description="Show current song")
    async def nowplaying(self, interaction: discord.Interaction):
        """Show current song"""
        try:
            player = self.get_player(interaction.guild_id)
            
            if player.current:
                embed = discord.Embed(title="🎵 Now Playing", color=discord.Color.green())
                embed.add_field(name="Title", value=player.current.title, inline=False)
                embed.add_field(name="URL", value=player.current.url, inline=False)
                if player.is_paused:
                    embed.add_field(name="Status", value="⏸️ Paused", inline=False)
                else:
                    embed.add_field(name="Status", value="▶️ Playing", inline=False)
                embed.add_field(name="Loop", value=player.loop_mode.capitalize(), inline=True)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("❌ Nothing is playing!")
        except Exception as e:
            logger.error(f'[MUSIC] NowPlaying error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="loop", description="Set loop mode")
    @app_commands.describe(mode="Loop mode: off, song, or queue")
    async def loop(self, interaction: discord.Interaction, mode: str):
        """Set loop mode"""
        try:
            player = self.get_player(interaction.guild_id)
            
            if mode.lower() not in ["off", "song", "queue"]:
                await interaction.response.send_message("❌ Mode must be: off, song, or queue", ephemeral=True)
                return
            
            player.loop_mode = mode.lower()
            
            emoji = {"off": "⭕", "song": "🔂", "queue": "🔁"}
            await interaction.response.send_message(f"{emoji.get(mode.lower(), '❓')} Loop mode set to: **{mode.capitalize()}**")
            logger.info(f'[MUSIC] Loop mode set to {mode}')
        except Exception as e:
            logger.error(f'[MUSIC] Loop error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="shuffle", description="Shuffle the queue")
    async def shuffle(self, interaction: discord.Interaction):
        """Shuffle the queue"""
        try:
            player = self.get_player(interaction.guild_id)
            
            if player.queue:
                songs = list(player.queue)
                random.shuffle(songs)
                player.queue = deque(songs)
                await interaction.response.send_message(f"🔀 Queue shuffled! ({len(songs)} songs)")
                logger.info(f'[MUSIC] Queue shuffled ({len(songs)} songs)')
            else:
                await interaction.response.send_message("❌ Queue is empty!")
        except Exception as e:
            logger.error(f'[MUSIC] Shuffle error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="saveplaylist", description="Save current queue as playlist")
    @app_commands.describe(name="Playlist name")
    async def save_playlist(self, interaction: discord.Interaction, name: str):
        """Save playlist"""
        try:
            player = self.get_player(interaction.guild_id)
            
            if not player.current and not player.queue:
                await interaction.response.send_message("❌ Queue is empty!")
                return
            
            playlists = load_playlists()
            user_id = str(interaction.user.id)
            
            if user_id not in playlists:
                playlists[user_id] = {}
            
            songs = []
            if player.current:
                songs.append({
                    "title": player.current.title,
                    "url": player.current.url,
                    "duration": player.current.duration
                })
            
            for song in player.queue:
                songs.append({
                    "title": song.title,
                    "url": song.url,
                    "duration": song.duration
                })
            
            playlists[user_id][name] = {
                "songs": songs,
                "created": str(datetime.now())
            }
            
            save_playlists(playlists)
            
            embed = discord.Embed(
                title="💾 Playlist Saved",
                description=f"Playlist **{name}** saved with {len(songs)} songs",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
            logger.info(f'[MUSIC] Playlist saved: {name} ({len(songs)} songs)')
        except Exception as e:
            logger.error(f'[MUSIC] Save playlist error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")

    @app_commands.command(name="loadplaylist", description="Load a saved playlist")
    @app_commands.describe(name="Playlist name")
    async def load_playlist(self, interaction: discord.Interaction, name: str):
        """Load playlist"""
        try:
            player = self.get_player(interaction.guild_id)
            playlists = load_playlists()
            user_id = str(interaction.user.id)
            
            if user_id not in playlists or name not in playlists[user_id]:
                await interaction.response.send_message("❌ Playlist not found!")
                return
            
            playlist = playlists[user_id][name]
            songs = playlist["songs"]
            
            # Add songs to queue
            for song_data in songs:
                song = Song(song_data["title"], song_data["url"], song_data["duration"])
                player.queue.append(song)
            
            embed = discord.Embed(
                title="📋 Playlist Loaded",
                description=f"Loaded playlist **{name}** with {len(songs)} songs",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
            logger.info(f'[MUSIC] Playlist loaded: {name} ({len(songs)} songs)')
        except Exception as e:
            logger.error(f'[MUSIC] Load playlist error: {e}')
            await interaction.response.send_message(f"❌ Error: {str(e)[:100]}")




async def setup(bot):
    await bot.add_cog(MusicCommands(bot))
