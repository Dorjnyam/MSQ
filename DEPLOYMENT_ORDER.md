# 🚀 Deploy хийх дараалал (Step-by-Step)

## ✅ Зөв дараалал

### Step 1: Frontend-ийг Vercel дээр deploy хийх

**Яагаад эхлээд frontend?**
- Frontend URL-ийг мэдэж авах
- Backend CORS тохируулахад хэрэгтэй

**⚠️ ЧУХАЛ: Таны repo (`Dorjnyam/MSQ`) дээр `frontend` болон `backend` хоёр folder байгаа тул Root Directory заавал тохируулах хэрэгтэй!**

**Алхам:**
1. [vercel.com/new](https://vercel.com/new) руу оч
2. GitHub repo-оо connect хийх: `Dorjnyam/MSQ`
3. **Root Directory**: `frontend` гэж бичих (эсвэл `./frontend`)
   - ⚠️ Энэ нь заавал шаардлагатай! Vercel-д зөвхөн `frontend` folder-ийг deploy хийхийг заах
4. Framework: Next.js (автоматаар илрүүлнэ)
5. Deploy хийх
6. Frontend URL-ийг тэмдэглэх (жишээ: `https://msq.vercel.app` эсвэл `https://msq-dorjnyam.vercel.app`)

### Step 2: Backend-ийг Fly.io дээр deploy хийх

**Алхам:**
1. `cd backend`
2. Environment variables тохируулах:
   ```bash
   fly secrets set GEMINI_API_KEY=your_key
   fly secrets set FRONTEND_URL=https://test-generator.vercel.app
   fly secrets set DEBUG=False
   ```
3. Deploy:
   ```bash
   fly deploy
   ```
4. Backend URL-ийг тэмдэглэх (жишээ: `https://test-generator-backend.fly.dev`)

### Step 3: Frontend-ийг дахин тохируулах

**Алхам:**
1. Vercel dashboard → Project → Settings → Environment Variables
2. `NEXT_PUBLIC_BACKEND_URL` нэмэх:
   ```
   Value: https://test-generator-backend.fly.dev
   ```
3. Redeploy хийх (Vercel dashboard дээр)

### Step 4: Test хийх

1. Frontend URL нээх
2. PDF upload хийх
3. MCQ generate хийх
4. Ажиллаж байгаа эсэхийг шалгах

## 📋 Checklist

### Frontend (Vercel)
- [ ] Vercel account үүсгэсэн
- [ ] GitHub repo connect хийсэн
- [ ] Root directory: `frontend` сонгосон
- [ ] Deploy хийсэн
- [ ] Frontend URL тэмдэглэсэн: `_________________`

### Backend (Fly.io)
- [ ] Fly CLI суулгасан
- [ ] `fly auth login` хийсэн
- [ ] `cd backend` хийсэн
- [ ] `GEMINI_API_KEY` тохируулсан
- [ ] `FRONTEND_URL` тохируулсан (Vercel URL)
- [ ] `fly deploy` хийсэн
- [ ] Backend URL тэмдэглэсэн: `_________________`

### Final Setup
- [ ] Vercel дээр `NEXT_PUBLIC_BACKEND_URL` тохируулсан
- [ ] Frontend redeploy хийсэн
- [ ] Test хийсэн - ажиллаж байна ✅

## 🔄 Хэрэв алдаа гарвал

### CORS алдаа:
```bash
# Backend дээр frontend URL-ийг шалгах
fly secrets list

# Зөв тохируулах
fly secrets set FRONTEND_URL=https://your-frontend.vercel.app
```

### API connection алдаа:
```bash
# Vercel дээр environment variable шалгах
# Vercel Dashboard → Settings → Environment Variables

# Зөв тохируулах
NEXT_PUBLIC_BACKEND_URL=https://your-backend.fly.dev
```

### Backend ажиллахгүй:
```bash
# Logs шалгах
fly logs

# Status шалгах
fly status
```

## 💡 Tips

1. **Environment Variables**: 
   - Vercel: `NEXT_PUBLIC_BACKEND_URL`
   - Fly.io: `FRONTEND_URL`, `GEMINI_API_KEY`

2. **URLs тэмдэглэх**: 
   - Frontend: `https://test-generator.vercel.app`
   - Backend: `https://test-generator-backend.fly.dev`

3. **Redeploy**: 
   - Environment variable өөрчлөхөд redeploy хийх хэрэгтэй

## 🎉 Бэлэн!

Одоо таны app production дээр ажиллаж байна!

- Frontend: Vercel (free tier)
- Backend: Fly.io (free tier)
- Database: ChromaDB (local, Fly.io дээр)

