# Discord Bot - Version 2.1 Improvements Guide

## 🎯 New Features & Improvements

### 🛡️ **Moderation Commands** (NEW)

Comprehensive moderation system with automatic logging and audit trails.

#### Commands:
- **`/ban <user> <reason>`** - Ban a user from the server
  - Admin permission required
  - All bans are logged to audit log
  
- **`/kick <user> <reason>`** - Kick a user from the server
  - Admin permission required
  - Logged in audit trail

- **`/warn <user> <reason>`** - Warn a user
  - 3 automatic warnings = automatic kick
  - Persists across restarts (stored in warns.json)
  - Moderator permission required

- **`/mute <user> <duration>`** - Mute user in voice channels
  - Duration in minutes (0 = permanent)
  - Auto-unmutes after duration
  - Moderator permission required

- **`/unmute <user>`** - Unmute a user
  - Moderator permission required

- **`/warns <user>`** - Check warnings for a user
  - Shows last 5 warnings
  - Display total warn count
  - Anyone can check

- **`/clearwarns <user>`** - Clear all warnings
  - Admin only
  - Useful for second chances

#### Features:
- ✅ Audit logging system (`audit_log.json`)
- ✅ Persistent warn storage (`warns.json`)
- ✅ Automatic kick after 3 warnings
- ✅ Time-based mute system
- ✅ Beautiful embed responses

---

### 🎵 **Music Player Improvements**

Enhanced music experience with advanced playback controls.

#### New Commands:
- **`/loop <mode>`** - Set loop mode
  - `off` - Don't loop (⭕)
  - `song` - Loop current song (🔂)
  - `queue` - Loop entire queue (🔁)
  - Shows in now playing screen

- **`/shuffle`** - Shuffle queue
  - Randomizes all songs in queue
  - Shows count of shuffled songs
  - Keeps current song in place

- **`/saveplaylist <name>`** - Save current queue as playlist
  - Saves with timestamps
  - User-specific (private)
  - Stored in `playlists.json`
  - Includes current + queued songs

- **`/loadplaylist <name>`** - Load a saved playlist
  - Adds all songs to queue
  - Shows count of loaded songs
  - User-specific access only

#### Features:
- ✅ Three loop modes
- ✅ Queue shuffle
- ✅ Persistent playlist storage
- ✅ User-specific playlists
- ✅ Loop state shown in now playing

---

### 🤖 **AI Commands Improvements**

Better error handling, rate limiting, and reliability.

#### Improvements:
- ✅ **Rate Limiting**: 5 requests per user per minute
- ✅ **Better Error Handling**: Clear error messages
- ✅ **Input Validation**: 1-1000 character limit
- ✅ **Response Chunking**: Auto-split long responses (2000 char limit)
- ✅ **Higher Temperature**: More creative responses (0.9 for imagine)
- ✅ **Detailed Logging**: Full error traces
- ✅ **Graceful Degradation**: Service recovery

#### Commands:
- **`/ask <question>`** - Ask AI a question
  - Improved error messages
  - Rate limited per user
  - 500 token responses
  - Auto-splits long answers

- **`/imagine <prompt>`** - Generate creative text
  - Higher creativity temperature (0.9)
  - Better for creative tasks
  - Rate limited
  - Detailed error feedback

---

### ⚡ **Performance Optimizations**

#### Implemented:
- ✅ User request rate limiting with sliding window
- ✅ Efficient warn storage with JSON
- ✅ Guild cleanup on bot leave
- ✅ Async audio extraction for music
- ✅ Better error handling prevents crashes
- ✅ Graceful fallback for missing services

#### Results:
- Reduced API calls
- Better memory usage
- Faster command response
- More stable under load

---

### 🔧 **Stability Improvements**

#### Bug Fixes & Enhancements:
- ✅ Guild validation checks
- ✅ Null pointer prevention
- ✅ Type hint improvements
- ✅ Better exception handling
- ✅ Automatic recovery from errors
- ✅ Detailed logging for debugging

#### New Safety Features:
- Error messages are rate-limited
- All user inputs validated
- Guild context verified before actions
- Graceful handling of missing permissions

---

## 📊 File Structure

```
discord bot/
├── bot.py                          # Main bot
├── requirements.txt                # Dependencies
├── .env                            # Configuration
├── warns.json                      # Warn storage
├── audit_log.json                  # Moderation logs
├── playlists.json                  # Saved playlists
├── cogs/
│   ├── moderation_commands.py     # NEW: Ban, kick, warn, mute
│   ├── music_commands.py          # Enhanced: Loop, shuffle, playlists
│   ├── ai_commands.py             # Improved: Better error handling
│   └── utility_commands.py        # Utility commands
└── web/                            # Web dashboard
```

---

## 🚀 Usage Examples

### Moderation
```
/warn @user Spamming
/warns @user
/mute @user 10           # Mute for 10 minutes
/loop queue              # Loop entire queue
/saveplaylist "My Chill Mix"
```

### Music
```
/play "Never Gonna Give You Up"
/shuffle
/saveplaylist "Summer Hits"
/loadplaylist "Summer Hits"
/loop song
```

### AI
```
/ask "What is Python?"        # Get answer
/imagine "A cyberpunk city"    # Generate creative text
```

---

## 📝 Configuration Files

### warns.json
Stores user warnings per guild:
```json
{
  "guild_id": {
    "user_id": [
      {
        "reason": "Spamming",
        "date": "2024-01-15T10:30:00",
        "by": "Moderator#1234"
      }
    ]
  }
}
```

### playlists.json
User-specific playlists:
```json
{
  "user_id": {
    "playlist_name": {
      "songs": [
        {
          "title": "Song Title",
          "url": "https://...",
          "duration": 180
        }
      ],
      "created": "2024-01-15T10:30:00"
    }
  }
}
```

### audit_log.json
Full moderation audit trail:
```json
[
  {
    "timestamp": "2024-01-15T10:30:00",
    "action": "BAN",
    "target": "User#1234",
    "target_id": "123456789",
    "moderator": "Admin#1234",
    "moderator_id": "987654321",
    "reason": "Toxic behavior"
  }
]
```

---

## ⚠️ Important Notes

1. **Rate Limiting**: AI commands are limited to 5 per user per minute
2. **Loop Modes**: Loop state persists only during current session
3. **Playlists**: User-specific, private to the user who saved them
4. **Warns**: Auto-kick happens after 3 warns per guild
5. **Audit Log**: Kept to last 1000 entries for performance
6. **FFmpeg Required**: For music playback
7. **Permissions**: Check moderator/admin roles before using mod commands

---

## 🐛 Troubleshooting

### Music Not Playing
- Ensure FFmpeg is installed
- Check bot has voice permissions
- Verify YouTube URL is valid
- Check bot is in voice channel

### AI Not Responding
- Check GROQ_API_KEY is set
- Wait if rate limited (5/min per user)
- Verify message under 1000 chars
- Check logs for API errors

### Mod Commands Not Working
- Verify bot has admin permissions
- Check user has appropriate role
- Ensure bot is higher in role hierarchy
- Try again with valid guild

---

## 📈 Future Improvements

Planned features:
- [ ] Filter/search playlists
- [ ] Bulk mute/unmute
- [ ] Warn expiration (auto-remove old warns)
- [ ] Streaming AI responses
- [ ] Music duration display
- [ ] Queue move/remove commands
- [ ] Reaction roles system
- [ ] Anti-spam detection

---

## 📞 Support

Check the following for issues:
1. `bot.log` - Console output and errors
2. `audit_log.json` - Moderation actions
3. `warns.json` - Warning records
4. Discord permissions and roles

---

**Last Updated**: Version 2.1  
**Status**: All systems operational ✅
