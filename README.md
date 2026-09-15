# Shpion (Spyfall) Telegram boti

Python 3.11+ va python-telegram-bot 21.11.1 asosidagi asinxron guruh o‘yini.
GPT yoki Gemini kerak emas: o‘yin mantiqi Python orqali ishlaydi, AI krediti sarflanmaydi.

## 1. Token va Telegram sozlamalari

1. Telegramdagi rasmiy [@BotFather](https://t.me/BotFather) botini oching.
2. `/newbot` yuboring, bot nomi va username tanlang.
3. Berilgan tokenni `.env` fayliga yozing. Uni GitHub yoki chatga yubormang.
4. Botni o‘yin guruhiga qo‘shing. Botga xabar yozish ruxsati kerak.
5. Har bir o‘yinchi botni shaxsiy ochib `/start` bosishi shart.

Oddiy foydalanishda botga administrator huquqi kerak emas. Privacy mode yoqilgan
holda ham komandalar va inline tugmalar ishlaydi. Guruhda boshqa botlar bo‘lsa,
komandani `/join@SizningBotUsername` shaklida yuboring. Oddiy savol-javobni
ishtirokchilar o‘zaro olib boradi; bot uni o‘qishi shart emas.

Lobbi yaratuvchisi bo‘lmagan administratorni tekshirishda Telegramning
`getChatMember` metodi ishlatiladi. Telegram bu tekshiruvning boshqa foydalanuvchilar
uchun ishonchli ishlashini bot administrator bo‘lganda kafolatlaydi. Zarur bo‘lsa
botni administrator qiling yoki boshqaruv komandalarini lobbi yaratuvchisi bajarsin.

## 2. PyCharm / Windows orqali ishga tushirish

ZIPni alohida papkaga chiqaring. Bu oldingi AI-chat botidan alohida loyiha.
PyCharm → **File → Open** → `main.py` turgan `spyfall-bot` papkasini tanlang.
**Alt+F12** orqali PowerShell terminalini oching va ketma-ket bajaring:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` faylini oching va haqiqiy tokenni kiriting:

```dotenv
BOT_TOKEN=your_token_here
```

Botni boshlang:

```powershell
.\.venv\Scripts\python.exe main.py
```

PyCharmning yashil Run tugmasidan foydalanish uchun:
**Settings → Project → Python Interpreter → Add Interpreter → Existing** orqali
loyihadagi `.venv\Scripts\python.exe` ni tanlang. So‘ng `main.py` ustida
o‘ng tugma → **Run 'main'**. Bir vaqtda terminal va Run orqali ikki nusxa ochmang.

Virtual muhit faollashtirilgan bo‘lsa, standart komandalar ham ishlaydi:

```bash
pip install -r requirements.txt
python main.py
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .env ichiga tokenni kiriting
python main.py
```

## 3. Birinchi o‘yin

Kamida uchta haqiqiy Telegram akkaunti kerak; bot akkauntlari qatnashmaydi.

1. Hamma botga shaxsiy `/start` yuboradi (yoki lobbidagi tugma orqali ochadi).
2. Guruhda bir kishi `/newgame` yozadi — interaktiv jonli lobbi ochiladi.
3. Ishtirokchilar **🙋 Qo‘shilish** tugmasini bosadi (lobbi xabari jonli yangilanadi).
4. Ixtiyoriy: yaratuvchi **⏱ Vaqt** tugmasi orqali o‘yin vaqtini belgilaydi.
5. Kamida 3 kishi bo‘lgach, **▶️ O‘yinni boshlash** tugmasi paydo bo‘ladi va o‘yin boshlanadi.
6. Har kim shaxsiy xabarda (DM) o‘z rolini spoiler (yashirin) ko‘rinishda oladi. Shpion esa 24 ta joy ro‘yxatini bitta tugma bilan ko‘ra oladi.
7. Guruhda bot tasodifiy birinchi savol beruvchini e’lon qiladi va savol-javob boshlanadi.
8. Gumon paydo bo‘lganda `/accuse` menyusidan gumonlanuvchini tanlang, keyin ovoz bering.
9. Shpion topilsa, unga shaxsiy chatida barcha 24 joy ko‘rsatilgan tugmalar va 30 soniya beriladi.

## Komandalar

| Komanda | Vazifasi |
|---|---|
| `/start` | Shaxsiy suhbatda interaktiv bosh menyu (qoidalar, maslahatlar, joylar); guruhda tanishtirish |
| `/help` | O‘yin qoidalari va yo‘riqnoma |
| `/newgame` | Guruh uchun interaktiv jonli lobbi ochish |
| `/join` | Lobbiga qo‘shilish (yoki tugma orqali) |
| `/leave` | Lobbidan chiqish (yoki tugma orqali) |
| `/players` | Ishtirokchilar va belgilangan vaqt |
| `/startgame` | Kamida 3 ishtirokchi bilan boshlash (yoki tugma orqali) |
| `/settime 8` | Faqat lobbida 2–30 daqiqa (yoki tugma orqali) |
| `/accuse @username` | Ishtirokchini ayblash |
| `/accuse` | Inline menyu; xabarga reply qilinsa, o‘sha odam ayblanadi |
| `/endgame` | Yaratuvchi yoki guruh administratori tomonidan bekor qilish |
| `/stats` | Guruh bo‘yicha o‘yinlar, shpion bo‘lish va g‘alabalar |
| `/locations` | Barcha mumkin bo‘lgan joylar va rollar |

## Qoidalar bo‘yicha aniq qarorlar

- Lobbi yaratuvchisi avtomatik qo‘shilmaydi; u ham «Qo‘shilish»ni bosadi.
- «O‘yinni boshlash»ni istalgan ishtirokchi bosishi mumkin. Vaqt va bekor qilish — faqat yaratuvchi yoki guruh admini uchun.
- Bitta shpion tasodifiy tanlanadi. Boshqalarning rollari joydagi ro‘yxatdan tanlanadi.
- Barcha DMlar avval tekshiriladi. Agar biror o‘yinchi botga `/start` bosmagan bo‘lsa, butun lobbi o‘chib ketmaydi; bot aynan o‘sha o‘yinchilarni ogohlantiradi va lobbini saqlab qoladi. Qayta boshlash uchun faqat botni ochib /start bosish va tugmani qayta bosish kifoya.
- Rol yoki joy guruhga o‘yin tugashidan oldin chiqarilmaydi.
- Yarim vaqtda va bir daqiqa qolganda eslatma bor. Ikki daqiqalik o‘yinda
  bu ikki eslatma bir xil bo‘lgani uchun faqat bir marta yuboriladi.
- Faqat ishtirokchi ayblaydi. O‘zini ayblay olmaydi. Username yo‘q yoki
  o‘zgargan bo‘lsa, menyu yoki reply usulidan foydalanadi.
- Bir o‘yinda bitta ovoz berish bo‘ladi. Ayblanuvchi ham ovoz beradi.
  Har kim bir marta ovoz beradi; ovozni o‘zgartirish mumkin emas.
- Tasdiq uchun **barcha ishtirokchilarning yarmidan ko‘pi** Ha deyishi kerak.
  Masalan, 3 kishida 2 ta, 4 kishida 3 ta, 10 kishida 6 ta Ha talab qilinadi.
  Ovoz bermaganlar Ha emas. Tenglik yoki yetarli ovoz yo‘qligi — shpion g‘alabasi.
- Hamma ovoz bersa natija darhol chiqadi, aks holda 30 soniya kutiladi.
  O‘yin vaqti 30 soniyadan kam qolgan bo‘lsa, ovoz berish qolgan vaqt bilan cheklanadi.
- Noto‘g‘ri odam ayblansa — shpion yutadi. Vaqt ayblovsiz tugasa — shpion yutadi.
- Shpion topilsa, joy hali guruhga oshkor qilinmaydi. Unga barcha 24 joy
  ko‘rsatilgan shaxsiy tugmalar va 30 soniya beriladi. Faqat bitta tanlov:
  to‘g‘ri — shpion, xato yoki vaqt tugashi — oddiy o‘yinchilar g‘alabasi.
- Oxirgi imkoniyatning DMi yetmasa, oddiy o‘yinchilar yutadi.
- Majburiy yoki texnik bekor qilish g‘alaba sifatida hisoblanmaydi.
- `/stats` faqat to‘liq yakunlangan o‘yinlarni hisoblaydi: oddiy o‘yinchilar
  yutsa, shpiondan boshqa hamma bittadan g‘alaba oladi.

## Papka tuzilishi

| Fayl/papka | Mas’uliyati |
|---|---|
| `main.py` | ApplicationBuilder, handlerlarni ulash, ishga tushirish |
| `game.py` | Telegramdan mustaqil holatlar va o‘yin qoidalari |
| `storage.py` | Storage protokoli, MemoryStorage, guruh qulflari |
| `service.py` | DM, taymerlar, yakunlash va natijalarni yuborish |
| `locations.py` | Joylar va rollar lug‘ati |
| `texts.py` | Foydalanuvchiga ko‘rinadigan o‘zbekcha matnlar |
| `keyboards.py` | Inline klaviaturalar |
| `handlers/lobby.py` | Lobbi komandalar |
| `handlers/game.py` | Boshlash, tugatish, yordam, statistika |
| `handlers/voting.py` | Ayblash, ovoz va oxirgi taxmin tugmalari |
| `handlers/common.py` | Guruh tekshiruvi, ruxsatlar, lock |
| `tests/` | Offline avtomatik tekshiruvlar |

## Saqlash va parallel o‘yinlar

Har bir `chat_id` uchun alohida o‘yin bor. Bir guruhning forum mavzulari
bitta guruh sessiyasini ulashadi. Bir odam turli guruhlarda qatnasha oladi;
DMlarda guruh nomi va sessiya kodi beriladi. Oxirgi taxmin tugmasi ham aniq
guruh/sessiyaga bog‘langan.

Har guruh uchun `asyncio.Lock` bor: callback va taymerlar bir holatni bir
vaqtda o‘zgartira olmaydi. Eski sessiya tugmalari va taymerlari yangi o‘yinga
ta’sir qilmaydi. Natija statistikasi bir martagina yoziladi. Tugashda barcha
sessiya joblari bekor qilinadi. Server kechikkanida ham deadline tekshiriladi.

Hamma ma’lumot **in-memory**: restartdan keyin o‘yinlar, vaqt sozlamalari va
statistika yo‘qoladi. Bitta bot tokeni uchun bitta process ishlating. SQLite
qo‘shish uchun `Storage` protokolini amalga oshiring va `main.py` dagi
`MemoryStorage()` ni almashtiring. Restartdan o‘yinlarni tiklash qo‘shilsa,
monotonic deadline o‘rniga saqlanadigan UTC vaqtlar va joblarni qayta tiklash
logikasi ham kerak bo‘ladi.

## Testlar

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
```

Testlarda Telegram xabarlari imitatsiya qilinadi, token kerak emas.
Sinov tafsilotlari `TESTING.md` da. Jonli tekshiruv uchun uchta akkaunt bilan
yuqoridagi birinchi o‘yin ketma-ketligini bajaring.

## Muammolar

- `BOT_TOKEN` xatosi: `.env` aynan `main.py` yonida bo‘lsin; `.env.txt` emas.
- `Conflict`: shu token bilan boshqa process yoki oldingi bot ishlayotganini tekshiring.
- DM kelmayapti: botga shaxsiy `/start` yuboring va blokdan chiqaring.
- Komanda ishlamayapti: guruhga botni qo‘shing; anonim administrator nomidan emas,
  shaxsiy akkauntdan komanda yuboring. Kerak bo‘lsa `@bot_username` qo‘shing.
- JobQueue xatosi: `pip install -r requirements.txt` ni qayta bajaring;
  `[job-queue]` qo‘shimchasi requirements ichida bor.
- SOCKS proxy ishlatsangiz: `pip install "python-telegram-bot[socks]==21.11.1"`.
- Kompyuter o‘chsa yoki internet uzilsa, bot ishlamaydi. Doimiy ishlash uchun
  keyinchalik serverda ishga tushiring.

Asosiy manbalar: [PTB 21.11.1](https://docs.python-telegram-bot.org/en/v21.11.1/),
[JobQueue](https://docs.python-telegram-bot.org/en/v21.11.1/telegram.ext.jobqueue.html).
