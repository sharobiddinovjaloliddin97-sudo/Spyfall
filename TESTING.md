# Tekshiruv natijalari

Muhit: Python 3.12, python-telegram-bot 21.11.1, JobQueue qo‘shimchasi.
Kod Python 3.11+ uchun yozilgan.

20 ta offline avtomatik test muvaffaqiyatli o‘tdi:

- 3–10 ishtirokchi chegarasi, takroriy qo‘shilish, chiqish va boshlash shartlari.
- 24 ta joy, yagona shpion, joyga mos oddiy rollar va emojilar.
- Ishtirokchi bo‘lmagan odamning ovozi/ayblovi, o‘zini ayblash va takroriy ovoz.
- Barcha ishtirokchilar bo‘yicha qat’iy ko‘pchilik, teng ovoz va noto‘g‘ri ayblov.
- Shpionning to‘g‘ri/xato taxmini, boshqa odamning taxmini va ikkinchi urinish.
- Ovoz berish hamda oxirgi taxmin vaqt chegaralari.
- Guruhlar holati/statistikasining ajratilishi va statistikani bir marta yozish.
- Rollarning faqat DMga spoiler ko‘rinishida ketishi, eslatmalar va taymerlar.
- Shaxsiy interaktiv bosh menyu navigatsiyasi (qoidalar, maslahatlar, lokatsiyalar).
- Shpionning shaxsiy chatda lokatsiyalar ro‘yxatini ko‘rish tugmasi.
- Lobbining inline tugmalar orqali boshqarilishi (chiqish, vaqt, qoidalar, qayta qo‘shilish).
- DM xatoligida lobbining buzilmasdan saqlanib qolishi va ogohlantirish berilishi.
- Bir vaqtda kelgan timeoutlar, takroriy ovoz va oxirgi taxminlar.
- Eski sessiya tugmalari/joblari yangi o‘yinga tegmasligi.
- Oxirgi imkoniyat va bekor qilishda joblarni tozalash.
- Callback payloadlarining 64 baytdan oshmasligi.
- ApplicationBuilder, JobQueue, post_init va barcha buyruqlar menyusining ulanishi.

Ruff tekshiruvi: E/F/I qoidalari, 79 belgilik satrlar; tarjima matnlari uchun
satr uzunligi istisnosi. Python sintaksisi compileall bilan tekshirildi.

## Qayta tekshirish

```bash
python -m unittest discover -v
python -m compileall -q .
```

Ixtiyoriy format tekshiruvi (`ruff` ishga tushirish uchun shart emas):

```bash
pip install ruff
ruff check .
ruff format --check .
```

## Jonli Telegram sinovi hali bajarilmagan

Testlar haqiqiy token yoki Telegram xabarlarini ishlatmaydi. Quyidagilarni
o‘z tokeningiz va uchta Telegram akkaunti bilan tekshiring:

1. Bitta akkaunt DMda `/start` bosmasin: bot aynan unga yozolmaganini bildirib,
   o‘yin urinishini bekor qilsin. Keyin hamma `/start` qilib qayta o‘ynasin.
2. Hamma qo‘shilsin; uch kishi uchta to‘g‘ri DM olsin, guruhga joy chiqmasin.
3. `/settime 2` bilan bir daqiqalik eslatma va timeoutni tekshiring.
4. Shpionni ayblab ko‘pchilik ovoz bering; uning to‘g‘ri/xato taxminini sinang.
5. Boshqa o‘yinda aybsiz odamni ayblang yoki ovoz bermang; shpion yutsin.
6. Bir paytda boshqa guruhda o‘yin oching va holatlar ajratilganini tekshiring.
7. `/endgame`, so‘ng eski tugmalar va `/stats` natijasini tekshiring.

DM va guruhga yetkazish Telegram tarmog‘i va ruxsatlariga bog‘liq. Bot restart
bo‘lsa, in-memory sessiyalar va statistika yo‘qoladi.
