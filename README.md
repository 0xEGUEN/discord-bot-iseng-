# Simple Discord Bot

Bot Discord sederhana dengan beberapa command dasar.

## Fitur

- `!ping` - Cek latency bot
- `!hello` - Ucapan sapaan
- `!echo <message>` - Echo pesan Anda
- `!info` - Info bot
- `!commands` - Daftar semua command

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Buat Bot Token
1. Buka [Discord Developer Portal](https://discord.com/developers/applications)
2. Klik "New Application" dan beri nama
3. Pergi ke tab "Bot" → "Add Bot"
4. Copy token dari "TOKEN" section

### 3. Setup Environment Variable
1. Rename `.env.example` menjadi `.env`
2. Paste bot token Anda:
```
DISCORD_TOKEN=your_token_here
```

### 4. Konfigurasi Bot Permissions
Di Developer Portal:
1. Pergi ke "OAuth2" → "URL Generator"
2. Pilih scope: `bot`
3. Pilih permissions: `Send Messages`, `Read Messages/View Channels`
4. Copy generated URL dan invite bot ke server Anda

### 5. Run Bot
```bash
python bot.py
```

Jika berhasil, Anda akan melihat: `[BotName] has connected to Discord!`

## Penggunaan

Di Discord server, ketik:
```
!ping          # Response: Pong! XXXms
!hello         # Response: Hello [username]! 👋
!echo hello    # Response: hello
!info          # Info bot dalam embed
!commands      # Daftar semua command
```

## Troubleshooting

**Bot tidak connect:**
- Cek DISCORD_TOKEN di `.env` sudah benar
- Cek bot sudah di-invite ke server

**Command tidak work:**
- Pastikan message content intent aktif di Developer Portal
- Cek command prefix benar (`!`)

## Struktur File
```
.
├── bot.py              # Main bot file
├── requirements.txt    # Dependencies
├── .env               # Environment variables (JANGAN di-commit)
├── .env.example       # Contoh .env
└── README.md          # File ini
```
