# Groq API Setup Guide

## Quick Setup - Groq (FREE & UNLIMITED)

Bot Anda sudah di-update untuk menggunakan **Groq** (pengganti OpenAI yang lebih cepat & gratis).

---

## 🚀 Step 1: Get Groq API Key (FREE!)

1. Buka: https://console.groq.com
2. Sign Up (gratis, no credit card needed)
3. Create New API Key
4. Copy key pada bagian "API Keys"

---

## 🔧 Step 2: Paste ke .env

Edit file `.env` di folder bot:

```
DISCORD_TOKEN=your_discord_token
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

Replace `gsk_xxxxxxxxxxxxx` dengan key dari Groq.

---

## 📝 Model yang Tersedia:

**Default kami pakai:** `mixtral-8x7b-32768` (sangat cepat & bagus)

Model lain yang Available:
- `mixtral-8x7b-32768` - Balanced, cepat
- `llama2-70b-4096` - Powerful, lebih lambat  
- `gemma-7b-it` - Ringan, cepat

Untuk ganti model, edit `bot.py` → cari `model="mixtral-8x7b-32768"` → ubah.

---

## ✅ Keuntungan Groq:

✓ FREE - Unlimited (no rate limit per user)  
✓ SUPER CEPAT - Inference speed terbaik  
✓ No Credit Card - Signup instant  
✓ Multiple Models - Pilih2 model terbaik  
✓ Simple API - Sama seperti OpenAI format  

---

## 🧪 Test Bot:

Setelah setup .env:

```bash
python bot.py
```

Coba di Discord:
```
!ask Apa itu AI?
```

Response akan instant! ⚡

---

## 📊 Limits:

Groq Free Tier:
- **30 requests/minute** (sangat banyak untuk personal bot)
- Unlimited total requests per hari
- No expiration

Cukup untuk bot personal/small server.

---

## ⚙️ Troubleshooting:

**Error: "GROQ_API_KEY not found"**
- Pastikan .env punya `GROQ_API_KEY=...`
- Pastikan format benar

**Error: "API Error"**
- Check internet connection
- Verify API key valid
- Check logs di `bot.log`

---

**Bot sekarang jalan dengan Groq - super cepat dan gratis!** 🎉
