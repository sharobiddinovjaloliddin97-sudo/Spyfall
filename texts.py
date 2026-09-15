"""User-facing Uzbek text. Add another locale dictionary to extend languages."""

UZ = {
    "private_start": (
        "🕵️ *Shpion (Spyfall) o‘yiniga xush kelibsiz!*\n\n"
        "Bu bot guruhlarda qiziqarli Shpion o‘yinini o‘tkazish uchun mo‘ljallangan.\n"
        "O‘yin davomida maxfiy rolingiz va joyingiz aynan shu yerga yuboriladi.\n\n"
        "Quyidagi tugmalar orqali qoidalar bilan tanishing yoki botni guruhingizga qo‘shing:"
    ),
    "group_start": (
        "🕵️ *Shpion (Spyfall) o‘yini!*\n\n"
        "Yangi o‘yin boshlash uchun /newgame yozing yoki pastdagi Menyudan foydalaning.\n"
        "Qoidalar: /help | Lokatsiyalar: /locations"
    ),
    "help": (
        "📖 *SHPION O‘YINI QOIDALARI*\n\n"
        "👥 *Ishtirokchilar:* 3 dan 10 tagacha\n"
        "⏱ *Vaqt:* 2–30 daqiqa (standart 8 daqiqa)\n\n"
        "🎯 *Maqsad:*\n"
        "• *Oddiy o‘yinchilar:* Hamma bir xil maxfiy joyda (masalan, Kasalxona, Samolyot) va har kimning o‘z roli bor. Maqsad — savol-javob orqali shpionni topish.\n"
        "• *Shpion:* Qayerdaligini bilmaydi! Maqsad — fosh bo‘lmaslik va suhbatdan maxfiy joy nomini aniqlash.\n\n"
        "💬 *O‘yin jarayoni:*\n"
        "1. Guruhda /newgame ochiladi, hamma «Qo‘shilish»ni bosadi.\n"
        "2. «O‘yinni boshlash» bosilgach, har kimga bot shaxsiyida roli yuboriladi.\n"
        "3. O‘yinchilar navbat bilan bir-biriga savol beradi (masalan: *«Ali, bu yerga har kuni kelasizmi?»*).\n"
        "4. Savolni shunday beringki, joy nomini aytib qo‘ymang, lekin o‘zingiz joyni bilishingizni boshqalar tushunsin.\n\n"
        "🗳 *Ayblash va Ovoz berish:*\n"
        "• Biror kishidan shubhalansangiz: /accuse yoki «Ayblash» menyusidan foydalaning.\n"
        "• Barcha ishtirokchilar 30 soniya ichida ovoz beradi. Yarmidan ko‘pi «Ha» desa, ayblov tasdiqlanadi.\n"
        "• Shpion topilsa — unga joyni topish uchun 30 soniya va bitta taxmin beriladi. Topsa shpion, topmasa oddiy o‘yinchilar yutadi!\n\n"
        "📌 *Asosiy buyruqlar:*\n"
        "/newgame — yangi lobbi | /players — o‘yinchilar\n"
        "/accuse — ayblash | /locations — 24 ta joy\n"
        "/stats — statistika | /endgame — o‘yinni to‘xtatish"
    ),
    "how_to_play": (
        "📖 *SHPION — QANDAY O‘YNALADI?*\n\n"
        "1️⃣ *Rollarni olish:*\n"
        "O‘yin boshlanganda bot har bir ishtirokchiga shaxsiy xabar yuboradi. Bitta tasodifiy o‘yinchi — *Shpion*, qolganlar esa ma’lum bir lokatsiyadagi xodimlar yoki mehmonlar bo‘ladi.\n\n"
        "2️⃣ *Savol-javob bosqichi:*\n"
        "Guruhda navbat bilan bir-biringizga savol berasiz:\n"
        "• *Savol beruvchi:* Istalgan kishiga savol beradi.\n"
        "• *Javob beruvchi:* Javob berib, keyingi savolni boshqa odamga yo‘llaydi (o‘ziga savol bergan odamga darhol qaytarib savol berish mumkin emas).\n\n"
        "3️⃣ *Shpionning vazifasi:*\n"
        "Diqqat bilan eshitish, umumiyroq javoblar berib o‘zini fosh qilmaslik va barcha gaplardan qaysi joydaligini topish.\n\n"
        "4️⃣ *Oddiy o‘yinchilarning vazifasi:*\n"
        "Shubhali, noaniq yoki g‘alati javob bergan kishini aniqlash va /accuse orqali ayblash!"
    ),
    "question_tips": (
        "💡 *SAVOL BERISH BO‘YICHA MASLAHATLAR*\n\n"
        "Yaxshi savol — joy nomini to‘g‘ridan-to‘g‘ri oshkor qilmaydigan, lekin o‘yinchining rolini sinovdan o‘tkazadigan savoldir.\n\n"
        "✅ *Yaxshi savol namunalari:*\n"
        "• *«Bu yerda maxsus forma yoki kiyim kiyiladimi?»*\n"
        "• *«Bu yerda odatda pul to‘lanadimi yoki xizmat tekinmi?»*\n"
        "• *«Bu joyga bolalar bilan kelish mumkinmi?»*\n"
        "• *«Bu yerda qattiq shovqin qilishga ruxsat bormi?»*\n"
        "• *«Bu yerga kechasi ham boriladimi?»*\n"
        "• *«Oxirgi marta bu joyga qachon bordingiz?»*\n\n"
        "❌ *Yomon savollar (joyni darhol sotib qo‘yadi):*\n"
        "• *«Samolyot qachon qo‘nadi?»* (Shpion joyni darhol bilib oladi)\n"
        "• *«Bemorlar ahvoli yaxshimi?»* (Kasalxona ekanligi fosh bo‘ladi)"
    ),
    "group_only": "Bu komanda faqat guruhda ishlaydi.",
    "human_only": "Komandani shaxsiy akkauntingizdan yuboring; anonim administrator rejimini o‘chiring.",
    "exists": "Bu guruhda o‘yin allaqachon bor. Qo‘shilish tugmasini bosing yoki /players yozing.",
    "missing": "Hozircha o‘yin yo‘q. /newgame bilan yangi lobbi oching.",
    "lobby_only": "Bu amal faqat o‘yin boshlanishidan oldin, lobbida bajariladi.",
    "active_only": "Hozir savol-javob bosqichi emas. O‘yinni lobbida boshlang.",
    "not_player": "Siz bu o‘yin ishtirokchisi emassiz.",
    "already_joined": "Siz allaqachon qo‘shilgansiz.",
    "full": "Lobbi to‘ldi: eng ko‘pi 10 ishtirokchi.",
    "minimum": "Boshlash uchun kamida 3 ishtirokchi kerak.",
    "owner_only": "Buni faqat lobbi yaratuvchisi yoki guruh administratori bajarishi mumkin.",
    "time_usage": "Namuna: /settime 8. Vaqt 2–30 daqiqa bo‘lishi kerak.",
    "time_set": "⏱ O‘yin vaqti {minutes} daqiqaga o‘zgartirildi.",
    "lobby": (
        "🕵️ *YANGI O‘YIN LOBBISI*\n"
        "👑 Yaratuvchi: *{name}*\n"
        "⏱ Belgilangan vaqt: *{minutes} daqiqa*\n\n"
        "👥 *Qo‘shilgan o‘yinchilar ({count}/10):*\n"
        "{player_list}\n\n"
        "{status_hint}"
    ),
    "lobby_waiting": "⚠️ _Boshlash uchun kamida 3 ishtirokchi kerak._",
    "lobby_ready": "✅ _O‘yinni boshlashga tayyor! Ishtirokchilar «▶️ O‘yinni boshlash»ni bosishi mumkin._",
    "join_button": "🙋 Qo‘shilish",
    "leave_button": "🚪 Chiqish",
    "start_button": "▶️ O‘yinni boshlash",
    "open_bot": "🤖 Botni faollashtirish",
    "how_to_button": "📖 Qoidalar",
    "tips_button": "💡 Maslahatlar",
    "locations_button": "📍 Joylar",
    "add_group_button": "➕ Guruhga qo‘shish",
    "back_button": "⬅️ Orqaga",
    "spy_locations_button": "📍 24 ta joy ro‘yxatini ko‘rish",
    "time_button": "⏱ {minutes} daqiqa",
    "joined": "✅ {name} qo‘shildi. Ishtirokchilar: {count}/10.",
    "left": "↩️ {name} lobbidan chiqdi. Qoldi: {count}.",
    "players": "👥 *Ishtirokchilar ({count}/10):*\n{names}\n\n⏱ Belgilangan vaqt: *{minutes} daqiqa*.",
    "empty": "Hozircha hech kim qo‘shilmadi.",
    "probe": "🕵️ «{group}» guruhida o‘yin boshlanmoqda. Rolingiz tayyorlanmoqda...",
    "dm_failed": (
        "⚠️ Quyidagi o‘yinchilarga shaxsiy xabar yuborib bo‘lmadi:\n"
        "*{names}*\n\n"
        "Iltimos, botni ochib /start bosing yoki blokdan chiqaring.\n"
        "So‘ng qayta *«▶️ O‘yinni boshlash»* tugmasini bosing!"
    ),
    "role": (
        "🕵️ Guruh: *{group}*\n"
        "🔑 O‘yin kodi: `{sid}`\n\n"
        "📍 Maxfiy joy: ||{location}||\n"
        "🎭 Rolingiz: ||{role}||\n\n"
        "💡 _Rol va joyni ko‘rish uchun ustiga bosing. Suhbat davomida joy nomini to‘g‘ridan-to‘g‘ri aytmasdan, shpionni aniqlashga harakat qiling!_"
    ),
    "spy_role": (
        "🕵️ Guruh: *{group}*\n"
        "🔑 O‘yin kodi: `{sid}`\n\n"
        "🤫 *SIZ SHPIONSIZ!*\n\n"
        "Siz qaysi joyda ekanligingizni bilmaysiz. Boshqalarning suhbatini diqqat bilan kuzatib, fosh bo‘lmaslikka va joy nomini taxmin qilishga harakat qiling!\n\n"
        "Quyidagi tugma orqali barcha mumkin bo‘lgan 24 ta joy ro‘yxatini ko‘rishingiz mumkin:"
    ),
    "started": (
        "🎮 *O‘YIN BOSHLANDI!*\n"
        "Rollar barchaga shaxsiy xabar orqali yuborildi.\n\n"
        "⏱ Vaqt: *{minutes} daqiqa*\n"
        "🎲 *Birinchi savolni {first_player} boshlaydi!*\n"
        "_Istalgan ishtirokchiga shubha uyg‘otmaydigan savol bering._\n\n"
        "Gumon bo‘lsa: /accuse yoki uning xabariga javoban /accuse yozing."
    ),
    "reminder": "⏱ O‘yin tugashiga taxminan *{minutes} daqiqa* qoldi.",
    "select_accused": "Kimni shpionlikda ayblamoqchisiz? Ismini tanlang:",
    "target_missing": "Bu ishtirokchi topilmadi. /accuse menyusidan tanlang yoki uning xabariga javoban /accuse yozing.",
    "self_accuse": "O‘zingizni ayblay olmaysiz.",
    "voting": (
        "🗳 *{accuser}* → *{accused}* ni aybladi!\n\n"
        "U haqiqatan ham shpionmi? *{seconds} soniya* ichida ovoz bering.\n"
        "Tasdiqlash uchun kamida *{needed} ta «Ha»* ovozi kerak."
    ),
    "yes": "✅ Ha, shpion",
    "no": "❌ Yo‘q",
    "voted": "Ovozingiz qabul qilindi.",
    "duplicate_vote": "Siz allaqachon ovoz bergansiz.",
    "stale": "Bu tugma eskirgan yoki bu bosqich yakunlangan.",
    "vote_result": "🗳 *Ovozlar natijasi:*\n✅ Ha: {yes} | ❌ Yo‘q: {no} | ⏳ Ovoz bermagan: {absent}.",
    "last_chance": "🕵️ *Shpion topildi!*\nUnga joyni taxmin qilish uchun 30 soniya berildi. Natijani kuting...",
    "guess_prompt": (
        "🕵️ *«{group}» — Oxirgi imkoniyat!*\n\n"
        "Siz fosh bo‘ldingiz, lekin 30 soniya ichida to‘g‘ri joyni topsangiz, g‘alaba qozonasiz!\n"
        "Faqat BITTA taxmin qabul qilinadi. Joyni tanlang:"
    ),
    "guess_saved": "Taxminingiz qabul qilindi.",
    "result": (
        "🏁 *O‘YIN YAKUNLANDI*\n\n"
        "🕵️ Shpion: *{spy}*\n"
        "📍 Maxfiy joy: *{location}*\n"
        "🏆 G‘olib: *{winner}*\n"
        "📝 {reason}\n\n"
        "Yana o‘ynash uchun: /newgame"
    ),
    "spy_winner": "Shpion",
    "civilians_winner": "Oddiy o‘yinchilar",
    "timeout_reason": "Vaqt tugadi, shpion aniqlanmadi.",
    "rejected_reason": "Ayblov yetarli «Ha» ovozini olmadi.",
    "wrong_person_reason": "Ayblangan o‘yinchi shpion emas edi.",
    "correct_guess_reason": "Shpion oxirgi imkoniyatda joyni to‘g‘ri topdi!",
    "wrong_guess_reason": "Shpion joyni noto‘g‘ri taxmin qildi.",
    "guess_timeout_reason": "Shpion belgilangan vaqtda joyni tanlamadi.",
    "guess_dm_failed_reason": "Shpionga oxirgi taxmin xabarini yetkazib bo‘lmadi.",
    "cancelled": "🛑 O‘yin bekor qilindi. /newgame bilan qayta boshlang.",
    "locations": "📍 *Barcha mumkin bo‘lgan joylar (24 ta):*\n\n{names}",
    "stats": "📊 *Guruh statistikasi:*\n\n{rows}",
    "stats_row": "👤 *{name}*: {games} o‘yin, {spy} marta shpion, {wins} g‘alaba",
    "stats_empty": "Hali yakunlangan o‘yinlar mavjud emas.",
    "error": "⚠️ Amal bajarilmadi. Birozdan so‘ng qayta urinib ko‘ring.",
    "token_missing": ".env faylida BOT_TOKEN ni kiriting.",
    "running": "Shpion boti ishga tushmoqda. To‘xtatish: Ctrl+C.",
    "startup_error": "Bot ishga tushmadi. Token, internet va boshqa bot nusxasi ishlamayotganini tekshiring.",
}


def tr(key, **values):
    return UZ[key].format(**values)

