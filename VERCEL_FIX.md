# 🔧 Vercel Build Error - Шууд Шийдэл

## ❌ Асуудал

Vercel root directory-аас build хийж байна:
```
Running "install" command: `npm install`...
# Root дээр package.json байхгүй!
```

## ✅ Шийдэл (2 арга)

### Арга 1: Vercel Dashboard дээр Root Directory тохируулах ⭐ (Хамгийн найдвартай)

1. [vercel.com/dashboard](https://vercel.com/dashboard) руу оч
2. Project-оо сонгох (`MSQ` эсвэл project name)
3. **Settings** → **General** tab
4. Scroll down → **Root Directory** хэсэг олох
5. `frontend` гэж бичих (эсвэл `./frontend`)
6. **Save** дар
7. **Deployments** tab → Latest deployment → **Redeploy**

### Арга 2: Root vercel.json ашиглах (Одоо байгаа)

Root folder дээр `vercel.json` файл үүсгэсэн. Энэ нь Vercel-д `frontend` folder-ийг ашиглахыг заана.

**GitHub руу push хийх:**
```bash
git add vercel.json
git commit -m "Add vercel.json for monorepo"
git push
```

Vercel автоматаар дахин deploy хийх ёстой.

## 🎯 Хамгийн хурдан шийдэл

**Vercel Dashboard дээр:**
1. Project → Settings → General
2. Root Directory: `frontend` бичих
3. Save
4. Redeploy

## ✅ Шалгах

Deploy хийсний дараа build logs дээр:

```
✅ Installing dependencies...
✅ Running "build" command...
✅ Build completed
```

Эсвэл:

```
✅ cd frontend && npm install
✅ cd frontend && npm run build
```

## 📝 Checklist

- [ ] Vercel Dashboard → Settings → General → Root Directory: `frontend` тохируулсан
- [ ] Save хийсэн
- [ ] Redeploy хийсэн
- [ ] Build амжилттай болсон ✅

## 🔄 Хэрэв асуудал үргэлжилвэл

### Project дахин үүсгэх:

1. Vercel Dashboard → **Add New** → **Project**
2. GitHub repo: `Dorjnyam/MSQ` сонгох
3. **Configure Project**:
   - **Root Directory**: `frontend` ⚠️ (ЭНЭ НЬ ЧУХАЛ!)
   - Framework: Next.js
4. Deploy

## 💡 Tips

- Root Directory тохируулах нь хамгийн найдвартай арга
- `vercel.json` нь backup арга
- Хоёулаа хийж болно (илүү найдвартай)

