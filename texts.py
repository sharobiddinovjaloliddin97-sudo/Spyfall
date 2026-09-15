"""User-facing Uzbek text. Add another locale dictionary to extend languages."""

UZ = {
    "private_start": (
        "🕵️ Shpion o‘yiniga xush kelibsiz! Endi sizga shaxsiy rol yubora olaman.\n"
        "Meni guruhga qo‘shing, /newgame bilan lobbi oching va /join yozing.\n"
        "Qoidalar: /help. Lokatsiyalar: /locations."
    ),
    "group_start": "🕵️ Shpion o‘yini! /newgame — lobbi ochish, /join — qo‘shilish, /help — qoidalar.",
    "help": (
        "🕵️ SHPION — 3–10 kishilik o‘yin\n\n"
        "1. Har kim avval botga shaxsiy /start yuboradi.\n"
        "2. Guruhda /newgame, so‘ng /join yoki Qo‘shilish tugmasi.\n"
        "3. Ishtirokchi /startgame yozadi: bitta shpion, boshqalarga joy va rol beriladi.\n"
        "4. Guruhda navbat bilan savol-javob qiling. Joyni oshkor qilmang!\n"
        "5. /accuse @username, xabarga javoban /accuse yoki /accuse menyusi bilan ayblang.\n"
        "6. Barcha ishtirokchilar, jumladan ayblanuvchi, bir martadan ovoz beradi. "
        "Yarmidan ko‘pi Ha desa ayblov tasdiqlanadi. Ovoz bermaganlar Ha hisoblanmaydi.\n"
        "7. Ovoz berish 30 soniya yoki qolgan o‘yin vaqti tugaguncha davom etadi. "
        "Hamma ovoz bersa, natija darhol chiqadi.\n"
        "8. Ayblov rad etilsa, noto‘g‘ri odam ayblansa yoki vaqt tugasa — shpion yutadi.\n"
        "9. Shpion topilsa, unga shaxsiy tugmalar orqali joyni topish uchun "
        "30 soniya va bitta taxmin beriladi. Topsa — shpion, topmasa — boshqalar yutadi.\n\n"
        "/leave — lobbidan chiqish\n/players — ishtirokchilar\n"
        "/settime 8 — 2–30 daqiqa (faqat lobbida)\n"
        "/endgame — bekor qilish (lobbi yaratuvchisi yoki guruh administratori)\n"
        "/stats — shu guruh statistikasi\n/locations — mumkin bo‘lgan joylar\n\n"
        "Bot qayta ishga tushsa, o‘yinlar va statistika tozalanadi."
    ),
    "group_only": "Bu komanda faqat guruhda ishlaydi.",
    "human_only": "Komandani shaxsiy akkauntingizdan yuboring; anonim administrator rejimini o‘chiring.",
    "exists": "Bu guruhda o‘yin allaqachon bor. /join yoki /players yozing.",
    "missing": "O‘yin yo‘q. /newgame bilan lobbi oching.",
    "lobby_only": "Bu amal faqat o‘yin boshlanishidan oldin, lobbida bajariladi.",
    "active_only": "Hozir savol-javob bosqichi emas. O‘yinni /startgame bilan boshlang.",
    "not_player": "Siz bu o‘yin ishtirokchisi emassiz.",
    "already_joined": "Siz allaqachon qo‘shilgansiz.",
    "full": "Lobbi to‘ldi: eng ko‘pi 10 ishtirokchi.",
    "minimum": "Boshlash uchun kamida 3 ishtirokchi kerak.",
    "owner_only": "Buni faqat lobbi yaratuvchisi yoki guruh administratori bajarishi mumkin.",
    "time_usage": "Namuna: /settime 8. Vaqt 2–30 daqiqa bo‘lishi kerak.",
    "time_set": "⏱ O‘yin vaqti {minutes} daqiqaga o‘zgartirildi.",
    "lobby": "🕵️ Yangi lobbi!\nYaratuvchi: {name}\n/join yoki tugma orqali qo‘shiling.\nAvval botga shaxsiy /start yuboring.",
    "join_button": "🙋 Qo‘shilish",
    "open_bot": "🤖 Botni shaxsiy ochish",
    "joined": "✅ {name} qo‘shildi. Ishtirokchilar: {count}/10.",
    "left": "↩️ {name} lobbidan chiqdi. Qoldi: {count}.",
    "players": "👥 Ishtirokchilar ({count}/10):\n{names}\n⏱ Belgilangan vaqt: {minutes} daqiqa.",
    "empty": "Hozircha hech kim yo‘q.",
    "probe": "🕵️ «{group}» guruhida o‘yin tayyorlanmoqda. Rol keyingi xabarda keladi.",
    "dm_failed": (
        "⚠️ {names} ga shaxsiy xabar yuborib bo‘lmadi. Botni ochib /start yuboring, "
        "bloklangan bo‘lsa blokdan chiqaring.\nBu urinish bekor qilindi; "
        "olingan rollar haqiqiy emas. Keyin /newgame bilan qayta boshlang."
    ),
    "role": "🕵️ Guruh: {group}\n🔑 O‘yin: {sid}\n📍 Joy: {location}\n🎭 Rolingiz: {role}\nJoyni oshkor qilmang; shpionni toping!",
    "spy_role": "🕵️ Guruh: {group}\n🔑 O‘yin: {sid}\nSiz SHPIONSIZ! Joyni suhbat orqali taxmin qilishga harakat qiling.\nMumkin bo‘lgan joylar: /locations.",
    "started": "🎮 O‘yin boshlandi! Rollar shaxsiy yuborildi.\n⏱ {minutes} daqiqa. Savol-javobni boshlang!\nShubha bo‘lsa: /accuse.",
    "reminder": "⏱ O‘yin tugashiga taxminan {minutes} daqiqa qoldi.",
    "select_accused": "Kimni ayblamoqchisiz? Ismini tanlang:",
    "target_missing": "Bu ishtirokchi topilmadi. /accuse menyusidan tanlang yoki uning xabariga javoban /accuse yozing.",
    "self_accuse": "O‘zingizni ayblay olmaysiz.",
    "voting": "🗳 {accuser} → {accused} ni aybladi!\nU shpionmi? {seconds} soniya ichida ovoz bering.\nTasdiqlash uchun kamida {needed} ta Ha ovozi kerak.",
    "yes": "✅ Ha, shpion",
    "no": "❌ Yo‘q",
    "voted": "Ovozingiz qabul qilindi.",
    "duplicate_vote": "Siz allaqachon ovoz berdingiz.",
    "stale": "Bu tugma eskirgan yoki bu bosqich tugagan.",
    "vote_result": "🗳 Ovozlar: Ha — {yes}, Yo‘q — {no}, ovoz bermagan — {absent}.",
    "last_chance": "🕵️ Shpion topildi! Unga joyni taxmin qilish uchun 30 soniya beriladi. Natijani kuting.",
    "guess_prompt": "🕵️ «{group}» — oxirgi imkoniyat!\n30 soniya ichida joyni tanlang. Faqat BITTA taxmin qabul qilinadi.",
    "guess_saved": "Taxminingiz qabul qilindi.",
    "result": "🏁 O‘YIN TUGADI\n\n🕵️ Shpion: {spy}\n📍 Joy: {location}\n🏆 G‘olib: {winner}\n📝 {reason}\n\nYana o‘ynash: /newgame",
    "spy_winner": "Shpion",
    "civilians_winner": "Oddiy o‘yinchilar",
    "timeout_reason": "Vaqt tugadi, shpion aniqlanmadi.",
    "rejected_reason": "Ayblov yetarli Ha ovozini olmadi.",
    "wrong_person_reason": "Ayblangan o‘yinchi shpion emas edi.",
    "correct_guess_reason": "Shpion oxirgi imkoniyatida joyni to‘g‘ri topdi.",
    "wrong_guess_reason": "Shpion joyni noto‘g‘ri taxmin qildi.",
    "guess_timeout_reason": "Shpion vaqtida joyni tanlamadi.",
    "guess_dm_failed_reason": "Shpionga oxirgi taxmin xabarini yetkazib bo‘lmadi.",
    "cancelled": "🛑 O‘yin bekor qilindi. Rollar endi haqiqiy emas. Statistika o‘zgarmadi. /newgame bilan qayta boshlang.",
    "locations": "📍 Mumkin bo‘lgan joylar:\n{names}",
    "stats": "📊 Guruh statistikasi\n{rows}",
    "stats_row": "{name}: {games} o‘yin, {spy} marta shpion, {wins} g‘alaba",
    "stats_empty": "Hali yakunlangan o‘yin yo‘q.",
    "error": "⚠️ Amal bajarilmadi. Birozdan keyin qayta urinib ko‘ring.",
    "token_missing": ".env faylida BOT_TOKEN ni kiriting.",
    "running": "Shpion boti ishga tushmoqda. To‘xtatish: Ctrl+C.",
    "startup_error": "Bot ishga tushmadi. Token, internet va boshqa bot nusxasi ishlamayotganini tekshiring.",
}


def tr(key, **values):
    return UZ[key].format(**values)
