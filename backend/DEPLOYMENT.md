# Fly.io Deployment Guide

## ✅ Алхам 1: Fly CLI суулгах

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Шалгах:**
```bash
fly --version
```

## ✅ Алхам 2: Fly.io-д нэвтрэх

```bash
fly auth login
```

Энэ нь browser нээж, танд нэвтрэх боломж олгоно.

## ✅ Алхам 3: Backend folder руу шилжих

```bash
cd backend
```

## ✅ Алхам 4: Environment Variables тохируулах

Fly.io-д environment variables тохируулах:

```bash
# GEMINI API Key (заавал шаардлагатай)
fly secrets set GEMINI_API_KEY=your_actual_gemini_api_key_here

# Frontend URL (production дээр frontend-ийн URL)
fly secrets set FRONTEND_URL=https://your-frontend-domain.vercel.app

# Бусад сонголттой тохиргоонууд
fly secrets set DEBUG=False
fly secrets set APP_NAME="PDF MCQ Generator"
```

**Бүх secrets-ийг нэг дор тохируулах:**
```bash
fly secrets set \
  GEMINI_API_KEY=your_key \
  FRONTEND_URL=https://your-frontend.vercel.app \
  DEBUG=False
```

## ✅ Алхам 5: Deploy хийх

```bash
fly deploy
```

Энэ нь:
- Docker image бүтээх
- Fly.io руу upload хийх
- App ажиллуулах
- Public URL өгөх (жишээ: `https://test-generator-backend.fly.dev`)

## ✅ Алхам 6: Logs шалгах

```bash
fly logs
```

## ✅ Алхам 7: App status шалгах

```bash
fly status
```

## ✅ Алхам 8: App нээх

```bash
fly open
```

Эсвэл browser дээр:
```
https://test-generator-backend.fly.dev
```

## 🔧 Асуудлыг шийдвэрлэх

### Port алдаа гарвал:
```bash
fly ssh console
# Дараа нь:
echo $PORT
```

### Environment variables шалгах:
```bash
fly ssh console
# Дараа нь:
env | grep GEMINI
```

### App restart хийх:
```bash
fly apps restart test-generator-backend
```

### Logs шалгах:
```bash
fly logs --app test-generator-backend
```

## 📝 Environment Variables жагсаалт

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | - | Google Gemini API key |
| `GEMINI_MODEL` | No | `gemini-2.5-flash` | Gemini model name |
| `FRONTEND_URL` | ✅ Yes | `http://localhost:3000` | Frontend URL (CORS) |
| `FRONTEND_URLS` | No | - | Multiple frontend URLs (comma-separated) |
| `DEBUG` | No | `True` | Debug mode |
| `CHROMA_DB_PATH` | No | `./chroma_db` | ChromaDB path |
| `MAX_FILE_SIZE` | No | `50` | Max file size (MB) |

## 🎯 Production тохиргоо

### CORS тохируулах:
```bash
# Нэг frontend URL
fly secrets set FRONTEND_URL=https://your-app.vercel.app

# Олон frontend URLs
fly secrets set FRONTEND_URLS=https://app1.vercel.app,https://app2.vercel.app
```

### Debug mode унтраах:
```bash
fly secrets set DEBUG=False
```

## 💰 Free Tier хязгаар

Fly.io Free Tier:
- ✅ 3 shared-CPU VMs (1 at a time)
- ✅ 256MB RAM (бид 512MB ашиглаж байна - free tier дээр ажиллана)
- ✅ ~3GB outbound bandwidth
- ⚠️ Sleep after inactivity (cold start)
- ⚠️ Slow cold starts

## 🚀 Next Steps

1. ✅ Backend deploy хийсэн
2. Frontend-ийг Vercel дээр deploy хийх
3. Frontend URL-ийг Fly.io secrets дээр тохируулах
4. Test хийх

## 📞 Тусламж

```bash
# Fly.io help
fly help

# App info
fly info

# SSH access
fly ssh console
```

