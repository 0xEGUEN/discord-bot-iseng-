# GitHub Pages Deployment Guide

## Static Frontend Deployment

Aplikasi frontend telah berhasil dikonfigurasi untuk deploy ke GitHub Pages. Files disimpan di folder `/docs` dan akan otomatis di-deploy ke `https://0xEGUEN.github.io/discord-bot-iseng-` setiap push ke branch `main`.

## Konfigurasi Backend API

Frontend dapat terhubung ke backend server yang terpisah. Ada 3 cara untuk mengatur URL backend:

### Opsi 1: Default Backend (Rekomendasi untuk Development)
Buka browser console dan jalankan:
```javascript
localStorage.setItem('API_BASE_URL', 'https://your-backend-url.com');
location.reload();
```

### Opsi 2: Environment Variable di GitHub Actions
Edit `.github/workflows/deploy.yml` dan tambahkan secrets, lalu gunakan untuk membuat environment file saat build.

### Opsi 3: Hardcode di index.html (Production)
Edit `docs/index.html` dan ubah baris:
```javascript
const API_BASE_URL = 'https://your-backend-url.com';
```

## Setup Backend untuk Deployment

Jika Anda ingin deploy backend juga, pertimbangkan:

1. **Heroku** - Free untuk hobby projects
   ```bash
   heroku create your-app-name
   heroku config:set DISCORD_TOKEN=your_token
   git push heroku main
   ```

2. **Render.com** - Free tier dengan auto-deploy dari GitHub
   - Connect repo ke Render
   - Set environment variables
   - Auto-deploy on push

3. **Railway.app** - $5/month credit free
   - Simple setup
   - GitHub integration

4. **Self-hosted** - VPS atau server sendiri

## Deploy Instructions

### Step 1: Push ke GitHub
```bash
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

### Step 2: Aktifkan GitHub Pages
- Pergi ke Settings repo
- Scroll ke "Pages"
- Pilih "Deploy from a branch"
- Branch: `gh-pages`, Folder: `/(root)`
- Tunggu sebentar, site akan live di `https://0xEGUEN.github.io/discord-bot-iseng-`

### Step 3: Konfigurasi Backend URL
1. Buka site di browser
2. Buka DevTools (F12)
3. Jalankan di console:
   ```javascript
   localStorage.setItem('API_BASE_URL', 'https://your-backend-api.com');
   location.reload();
   ```

## Testing Bot Status

Jika backend sedang offline atau tidak dikonfigurasi, status akan menunjukkan "Unable to check". Ini normal untuk frontend-only deployment.

Untuk full functionality:
1. Deploy aplikasi Flask ke server terpisah
2. Pastikan CORS di-enable di Flask backend
3. Atur API_BASE_URL di frontend

## CORS Setup di Flask Backend

Tambahkan ke `app.py`:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS untuk semua routes
```

Install: `pip install flask-cors`

## File Structure
```
docs/
  └── index.html (Frontend statis)
.github/
  └── workflows/
      └── deploy.yml (Otomatis deploy ke GH Pages)
```

Setiap push ke `main` branch akan otomatis di-deploy ke GitHub Pages!
