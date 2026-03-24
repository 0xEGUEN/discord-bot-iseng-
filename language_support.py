"""
Language support module for the bot
"""

TRANSLATIONS = {
    "en": {
        "greeting": "Hello",
        "success": "Success",
        "error": "Error",
        "music_play": "Now playing",
        "music_queue_added": "Added to queue",
        "music_not_found": "No results found",
        "music_paused": "Music paused",
        "music_resumed": "Music resumed",
        "music_stopped": "Music stopped",
        "music_skipped": "Skipped to next song",
        "voice_channel_required": "You need to be in a voice channel first",
        "nothing_playing": "Nothing is playing",
        "bot_not_connected": "Bot is not connected to a voice channel",
    },
    "id": {
        "greeting": "Halo",
        "success": "Berhasil",
        "error": "Kesalahan",
        "music_play": "Sedang memutar",
        "music_queue_added": "Ditambahkan ke antrian",
        "music_not_found": "Tidak ada hasil yang ditemukan",
        "music_paused": "Musik dijeda",
        "music_resumed": "Musik dilanjutkan",
        "music_stopped": "Musik dihentikan",
        "music_skipped": "Lanjut ke lagu berikutnya",
        "voice_channel_required": "Anda harus berada di saluran suara terlebih dahulu",
        "nothing_playing": "Tidak ada yang diputar",
        "bot_not_connected": "Bot tidak terhubung ke saluran suara",
    }
}

def get_language(lang_code):
    """Get translations for a specific language"""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS["en"])

def translate(key, lang_code="en"):
    """Translate a key to a specific language"""
    lang = get_language(lang_code)
    return lang.get(key, key)
