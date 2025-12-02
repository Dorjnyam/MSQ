# 🚀 Fly.io Quick Deploy Guide

## ⚠️ Чухал: Root folder-ийн fly.toml-ийг устгах эсвэл үл тоомсорлох

Root folder дээр `fly.toml` байгаа боловч **backend folder доторх fly.toml-ийг ашиглах хэрэгтэй**.

## ✅ Deploy хийх алхам

### 1. Backend folder руу шилжих
```bash
cd backend
```

### 2. Fly.io-д нэвтрэх (хэрэв нэвтрээгүй бол)
```bash
fly auth login
```

### 3. Environment Variables тохируулах
```bash
# GEMINI API Key (заавал шаардлагатай!)
fly secrets set GEMINI_API_KEY=your_actual_api_key_here

# Frontend URL (production дээр)
fly secrets set FRONTEND_URL=https://your-frontend.vercel.app

# Debug mode унтраах
fly secrets set DEBUG=False
```

### 4. Deploy хийх
```bash
fly deploy
```

### 5. Logs шалгах
```bash
fly logs
```

## 🔍 Асуудал гарвал

### App ажиллахгүй байвал:
```bash
fly status
fly logs
```

### Port алдаа:
- Fly.io автоматаар port 8080 ашиглана
- Dockerfile дээр PORT environment variable тохируулсан

### Environment variables алдаа:
```bash
fly ssh console
env | grep GEMINI
```

### App restart:
```bash
fly apps restart test-generator-backend
```

## 📝 Хийгдсэн сайжруулалтууд

1. ✅ `fly.toml` - Fly.io тохиргоо сайжруулсан
2. ✅ `Dockerfile` - Port environment variable нэмсэн
3. ✅ CORS - Олон frontend URLs дэмжих
4. ✅ Health check endpoint (`/`)

## 🎯 Дараагийн алхам

1. Deploy хийх
2. Frontend-ийг Vercel дээр deploy хийх
3. Frontend URL-ийг Fly.io secrets дээр тохируулах
4. Test хийх

