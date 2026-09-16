"""User-facing localized text (Uzbek and Russian)."""

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
    "lang_button": "🌐 Til: {lang_name}",
    "choose_lang": "🌐 Tilni tanlang / Выберите язык:",
    "lang_changed": "✅ Guruh tili o‘zgartirildi: {lang_name}",
    "user_lang_changed": "✅ Til o‘zgartirildi: {lang_name}",
    "lang_uz": "🇺🇿 O‘zbekcha",
    "lang_ru": "🇷🇺 Русский",
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

RU = {
    "private_start": (
        "🕵️ *Добро пожаловать в игру Шпион (Spyfall)!*\n\n"
        "Этот бот предназначен для проведения игры «Шпион» в группах.\n"
        "Во время игры ваша секретная роль и локация будут отправлены сюда.\n\n"
        "Используйте кнопки ниже, чтобы ознакомиться с правилами или добавить бота в группу:"
    ),
    "group_start": (
        "🕵️ *Игра Шпион (Spyfall)!*\n\n"
        "Чтобы начать новую игру, напишите /newgame или используйте Меню ниже.\n"
        "Правила: /help | Локации: /locations"
    ),
    "help": (
        "📖 *ПРАВИЛА ИГРЫ ШПИОН*\n\n"
        "👥 *Игроки:* от 3 до 10 человек\n"
        "⏱ *Время:* 2–30 минут (по умолчанию 8 минут)\n\n"
        "🎯 *Цель игры:*\n"
        "• *Обычные игроки:* Все находятся в одной секретной локации (например, Больница, Самолет) и имеют определенную профессию. Цель — путем вопросов и ответов вычислить шпиона.\n"
        "• *Шпион:* Не знает локацию! Цель — не выдать себя и догадаться о локации из разговора.\n\n"
        "💬 *Ход игры:*\n"
        "1. В группе создается лобби командой /newgame, все нажимают «Присоединиться».\n"
        "2. После нажатия «Начать игру» каждому игроку в ЛС отправляется роль.\n"
        "3. Игроки по очереди задают друг другу вопросы (например: *«Али, ты часто здесь бываешь?»*).\n"
        "4. Задавайте вопросы так, чтобы не выдать название локации, но показать остальным, что вы в курсе.\n\n"
        "🗳 *Обвинение и Голосование:*\n"
        "• Если вы подозреваете кого-то: используйте /accuse или кнопку обвинения.\n"
        "• Все участники голосуют в течение 30 секунд. Если большинство ответит «Да», обвинение подтверждается.\n"
        "• Если шпион найден — у него есть 30 секунд и одна попытка угадать локацию. Угадает — побеждает шпион, ошибется — побеждают мирные!\n\n"
        "📌 *Основные команды:*\n"
        "/newgame — новое лобби | /players — список игроков\n"
        "/accuse — обвинить | /locations — 24 локации\n"
        "/stats — статистика | /endgame — остановить игру"
    ),
    "how_to_play": (
        "📖 *ШПИОН — КАК ИГРАТЬ?*\n\n"
        "1️⃣ *Получение ролей:*\n"
        "В начале игры бот отправляет каждому игроку личное сообщение. Один случайный игрок становится *Шпионом*, а остальные получают локацию и роли сотрудников или гостей.\n\n"
        "2️⃣ *Раунд вопросов и ответов:*\n"
        "В группе игроки по очереди задают друг другу вопросы:\n"
        "• *Спрашивающий:* задает вопрос любому игроку.\n"
        "• *Отвечающий:* отвечает и задает следующий вопрос другому человеку (нельзя сразу возвращать вопрос тому, кто спросил вас).\n\n"
        "3️⃣ *Задача шпиона:*\n"
        "Внимательно слушать, давать общие и уклончивые ответы, не вызывая подозрений, и попытаться понять, где все находятся.\n\n"
        "4️⃣ *Задача мирных игроков:*\n"
        "Вычислить того, кто отвечает неуверенно или странно, и обвинить его через /accuse!"
    ),
    "question_tips": (
        "💡 *СОВЕТЫ ПО ВОПРОСАМ*\n\n"
        "Хороший вопрос — тот, который прямо не раскрывает локацию, но проверяет роль собеседника.\n\n"
        "✅ *Примеры хороших вопросов:*\n"
        "• *«Здесь нужна специальная форма или одежда?»*\n"
        "• *«Здесь обычно платят деньгами или вход бесплатный?»*\n"
        "• *«Сюда можно приходить с детьми?»*\n"
        "• *«Здесь разрешено громко шуметь?»*\n"
        "• *«Это место работает ночью?»*\n"
        "• *«Когда вы в последний раз здесь были?»*\n\n"
        "❌ *Плохие вопросы (сразу выдают локацию):*\n"
        "• *«Когда приземлится самолет?»* (Шпион сразу поймет локацию)\n"
        "• *«Как самочувствие пациентов?»* (Сразу понятно, что это больница)"
    ),
    "group_only": "Эта команда работает только в группе.",
    "human_only": "Отправляйте команду от личного аккаунта; отключите режим анонимного администратора.",
    "exists": "В этой группе игра уже создана. Нажмите кнопку «Присоединиться» или напишите /players.",
    "missing": "Сейчас игры нет. Создайте лобби командой /newgame.",
    "lobby_only": "Это действие доступно только до начала игры, в лобби.",
    "active_only": "Сейчас не раунд вопросов и ответов. Начните игру в лобби.",
    "not_player": "Вы не являетесь участником этой игры.",
    "already_joined": "Вы уже присоединились.",
    "full": "Лобби заполнено: максимум 10 игроков.",
    "minimum": "Для начала нужно минимум 3 игрока.",
    "owner_only": "Это действие может выполнить только создатель лобби или администратор группы.",
    "time_usage": "Пример: /settime 8. Время должно быть от 2 до 30 минут.",
    "time_set": "⏱ Время игры изменено на {minutes} мин.",
    "lobby": (
        "🕵️ *ЛОББИ НОВОЙ ИГРЫ*\n"
        "👑 Создатель: *{name}*\n"
        "⏱ Время раунда: *{minutes} минут*\n\n"
        "👥 *Игроки ({count}/10):*\n"
        "{player_list}\n\n"
        "{status_hint}"
    ),
    "lobby_waiting": "⚠️ _Для начала нужно минимум 3 игрока._",
    "lobby_ready": "✅ _Готовы к началу! Участники могут нажать «▶️ Начать игру»._",
    "join_button": "🙋 Присоединиться",
    "leave_button": "🚪 Выйти",
    "start_button": "▶️ Начать игру",
    "open_bot": "🤖 Активировать бота",
    "how_to_button": "📖 Правила",
    "tips_button": "💡 Советы",
    "locations_button": "📍 Локации",
    "add_group_button": "➕ Добавить в группу",
    "back_button": "⬅️ Назад",
    "spy_locations_button": "📍 Список всех 24 локаций",
    "time_button": "⏱ {minutes} мин",
    "lang_button": "🌐 Язык: {lang_name}",
    "choose_lang": "🌐 Выберите язык / Tilni tanlang:",
    "lang_changed": "✅ Язык группы изменен: {lang_name}",
    "user_lang_changed": "✅ Язык изменен: {lang_name}",
    "lang_uz": "🇺🇿 O‘zbekcha",
    "lang_ru": "🇷🇺 Русский",
    "joined": "✅ {name} присоединился. Игроков: {count}/10.",
    "left": "↩️ {name} покинул лобби. Осталось: {count}.",
    "players": "👥 *Игроки ({count}/10):*\n{names}\n\n⏱ Установленное время: *{minutes} минут*.",
    "empty": "Пока никто не присоединился.",
    "probe": "🕵️ В группе «{group}» начинается игра. Ваша роль готовится...",
    "dm_failed": (
        "⚠️ Не удалось отправить личное сообщение следующим игрокам:\n"
        "*{names}*\n\n"
        "Пожалуйста, откройте бота и нажмите /start или разблокируйте его.\n"
        "Затем снова нажмите *«▶️ Начать игру»*!"
    ),
    "role": (
        "🕵️ Группа: *{group}*\n"
        "🔑 Код игры: `{sid}`\n\n"
        "📍 Секретная локация: ||{location}||\n"
        "🎭 Ваша роль: ||{role}||\n\n"
        "💡 _Нажмите на текст, чтобы увидеть локацию и роль. В разговоре не называйте место прямо, вычисляйте шпиона!_"
    ),
    "spy_role": (
        "🕵️ Группа: *{group}*\n"
        "🔑 Код игры: `{sid}`\n\n"
        "🤫 *ВЫ ШПИОН!*\n\n"
        "Вы не знаете, где находитесь. Внимательно слушайте разговоры, не выдавайте себя и попытайтесь угадать локацию!\n\n"
        "Кнопка ниже покажет список всех возможных 24 локаций:"
    ),
    "started": (
        "🎮 *ИГРА НАЧАЛАСЬ!*\n"
        "Роли разосланы всем в личные сообщения.\n\n"
        "⏱ Время: *{minutes} минут*\n"
        "🎲 *Первый вопрос задает {first_player}!*\n"
        "_Задайте вопрос любому участнику, не вызывая подозрений._\n\n"
        "Если есть подозрения: /accuse или ответьте на сообщение подозреваемого командой /accuse."
    ),
    "reminder": "⏱ До конца игры осталось примерно *{minutes} мин*.",
    "select_accused": "Кого вы подозреваете в шпионаже? Выберите имя:",
    "target_missing": "Этот игрок не найден. Выберите из меню /accuse или ответьте на его сообщение командой /accuse.",
    "self_accuse": "Вы не можете обвинить самого себя.",
    "voting": (
        "🗳 *{accuser}* обвиняет → *{accused}*!\n\n"
        "Он действительно шпион? Проголосуйте за *{seconds} секунд*.\n"
        "Для подтверждения нужно минимум *{needed} голосов «Да»*."
    ),
    "yes": "✅ Да, шпион",
    "no": "❌ Нет",
    "voted": "Ваш голос принят.",
    "duplicate_vote": "Вы уже проголосовали.",
    "stale": "Эта кнопка устарела или этот этап уже завершен.",
    "vote_result": "🗳 *Результаты голосования:*\n✅ Да: {yes} | ❌ Нет: {no} | ⏳ Не голосовали: {absent}.",
    "last_chance": "🕵️ *Шпион найден!*\nЕму дается 30 секунд, чтобы угадать локацию. Ожидайте результата...",
    "guess_prompt": (
        "🕵️ *«{group}» — Последний шанс!*\n\n"
        "Вас раскрыли, но если за 30 секунд вы выберете правильную локацию, вы победите!\n"
        "Принимается только ОДНА попытка. Выберите локацию:"
    ),
    "guess_saved": "Ваша догадка принята.",
    "result": (
        "🏁 *ИГРА ОКОНЧЕНА*\n\n"
        "🕵️ Шпион: *{spy}*\n"
        "📍 Локация: *{location}*\n"
        "🏆 Победитель: *{winner}*\n"
        "📝 {reason}\n\n"
        "Сыграть снова: /newgame"
    ),
    "spy_winner": "Шпион",
    "civilians_winner": "Обычные игроки",
    "timeout_reason": "Время вышло, шпион не был найден.",
    "rejected_reason": "Обвинение не набрало достаточного количества голосов «Да».",
    "wrong_person_reason": "Обвиненный игрок не был шпионом.",
    "correct_guess_reason": "Шпион в последний момент правильно угадал локацию!",
    "wrong_guess_reason": "Шпион выбрал неверную локацию.",
    "guess_timeout_reason": "Шпион не успел выбрать локацию вовремя.",
    "guess_dm_failed_reason": "Не удалось доставить сообщение с выбором локации шпиону.",
    "cancelled": "🛑 Игра отменена. Начните заново с помощью /newgame.",
    "locations": "📍 *Все возможные локации (24):*\n\n{names}",
    "stats": "📊 *Статистика группы:*\n\n{rows}",
    "stats_row": "👤 *{name}*: {games} игр, {spy} раз шпион, {wins} побед",
    "stats_empty": "Завершенных игр пока нет.",
    "error": "⚠️ Действие не выполнено. Повторите попытку позже.",
    "token_missing": "Укажите BOT_TOKEN в файле .env.",
    "running": "Бот Шпион запускается. Остановка: Ctrl+C.",
    "startup_error": "Бот не запустился. Проверьте токен, интернет и другие запущенные копии бота.",
}

LOCALES = {
    "uz": UZ,
    "ru": RU,
}


def tr(key, lang="uz", **values):
    locale = LOCALES.get(lang, UZ)
    template = locale.get(key, UZ.get(key, key))
    return template.format(**values)


