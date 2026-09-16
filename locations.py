"""Add or remove locations here; every location needs at least one role."""

LOCATIONS_UZ = {
    "Restoran": ("Ofitsiant", "Oshpaz", "Mijoz", "Menejer"),
    "Samolyot": ("Uchuvchi", "Styuard", "Yo‘lovchi", "Ikkinchi uchuvchi"),
    "Maktab": ("O‘qituvchi", "O‘quvchi", "Direktor", "Kutubxonachi"),
    "Kasalxona": ("Shifokor", "Hamshira", "Bemor", "Jarroh"),
    "Konsert": ("Xonanda", "Tomoshabin", "Ovoz rejissyori", "Musiqachi"),
    "Kosmik stansiya": ("Kosmonavt", "Muhandis", "Olim", "Qo‘mondon"),
    "Poyezd": ("Mashinist", "Yo‘lovchi", "Kuzatuvchi", "Nazoratchi"),
    "Plyaj": ("Dam oluvchi", "Qutqaruvchi", "Sotuvchi", "Suzuvchi"),
    "Bank": ("Kassir", "Mijoz", "Qo‘riqchi", "Boshqaruvchi"),
    "Sirk": ("Masxaraboz", "Akrobat", "Tomoshabin", "Hayvon o‘rgatuvchi"),
    "Mehmonxona": ("Mehmon", "Administrator", "Farrosh", "Yuk tashuvchi"),
    "Supermarket": ("Kassir", "Xaridor", "Sotuvchi", "Omborchi"),
    "Universitet": ("Talaba", "Professor", "Dekan", "Laborant"),
    "Politsiya bo‘limi": ("Tergovchi", "Navbatchi", "Guvoh", "Politsiyachi"),
    "Kinoteatr": (
        "Tomoshabin",
        "Chipta sotuvchi",
        "Kinomexanik",
        "Nazoratchi",
    ),
    "Teatr": ("Aktyor", "Rejissyor", "Tomoshabin", "Grimchi"),
    "Muzey": ("Ekskursovod", "Sayyoh", "Qo‘riqchi", "Restavrator"),
    "Kutubxona": ("Kutubxonachi", "Kitobxon", "Talaba", "Arxivchi"),
    "Stadion": ("Futbolchi", "Hakam", "Muxlis", "Murabbiy"),
    "Hayvonot bog‘i": ("Veterinar", "Mehmon", "Qarovchi", "Qo‘riqchi"),
    "Ferma": ("Fermer", "Veterinar", "Traktorchi", "Ishchi"),
    "Qurilish maydoni": (
        "Quruvchi",
        "Muhandis",
        "Arxitektor",
        "Kran haydovchisi",
    ),
    "Kema": ("Kapitan", "Dengizchi", "Yo‘lovchi", "Oshpaz"),
    "Tog‘ lageri": ("Alpinist", "Yo‘lboshchi", "Sayyoh", "Qutqaruvchi"),
}

LOCATIONS_RU = {
    "Ресторан": ("Официант", "Повар", "Клиент", "Менеджер"),
    "Самолет": ("Пилот", "Стюардесса", "Пассажир", "Второй пилот"),
    "Школа": ("Учитель", "Ученик", "Директор", "Библиотекарь"),
    "Больница": ("Врач", "Медсестра", "Пациент", "Хирург"),
    "Концерт": ("Певец", "Зритель", "Звукорежиссер", "Музыкант"),
    "Космическая станция": ("Космонавт", "Инженер", "Ученый", "Командир"),
    "Поезд": ("Машинист", "Пассажир", "Проводник", "Контролер"),
    "Пляж": ("Отдыхающий", "Спасатель", "Продавец", "Пловец"),
    "Банк": ("Кассир", "Клиент", "Охранник", "Управляющий"),
    "Цирк": ("Клоун", "Акробат", "Зритель", "Дрессировщик"),
    "Отель": ("Гость", "Администратор", "Уборщик", "Носильщик"),
    "Супермаркет": ("Кассир", "Покупатель", "Продавец", "Кладовщик"),
    "Университет": ("Студент", "Профессор", "Декан", "Лаборант"),
    "Полицейский участок": (
        "Следователь",
        "Дежурный",
        "Свидетель",
        "Полицейский",
    ),
    "Кинотеатр": ("Зритель", "Кассир", "Киномеханик", "Контролер"),
    "Театр": ("Актер", "Режиссер", "Зритель", "Гример"),
    "Музей": ("Экскурсовод", "Турист", "Охранник", "Реставратор"),
    "Библиотека": ("Библиотекарь", "Читатель", "Студент", "Архивариус"),
    "Стадион": ("Футболист", "Судья", "Болельщик", "Тренер"),
    "Зоопарк": ("Ветеринар", "Посетитель", "Смотритель", "Охранник"),
    "Ферма": ("Фермер", "Ветеринар", "Тракторист", "Рабочий"),
    "Стройплощадка": (
        "Строитель",
        "Инженер",
        "Архитектор",
        "Крановщик",
    ),
    "Корабль": ("Капитан", "Матрос", "Пассажир", "Повар"),
    "Горный лагерь": ("Альпинист", "Проводник", "Турист", "Спасатель"),
}

LOCATIONS = LOCATIONS_UZ

LOCATION_EMOJIS = {
    # Uzbek
    "Restoran": "🍽",
    "Samolyot": "✈️",
    "Maktab": "🏫",
    "Kasalxona": "🏥",
    "Konsert": "🎤",
    "Kosmik stansiya": "🚀",
    "Poyezd": "🚆",
    "Plyaj": "🏖",
    "Bank": "🏦",
    "Sirk": "🎪",
    "Mehmonxona": "🏨",
    "Supermarket": "🛒",
    "Universitet": "🎓",
    "Politsiya bo‘limi": "👮‍♂️",
    "Kinoteatr": "🎬",
    "Teatr": "🎭",
    "Muzey": "🏛",
    "Kutubxona": "📚",
    "Stadion": "⚽️",
    "Hayvonot bog‘i": "🦁",
    "Ferma": "🚜",
    "Qurilish maydoni": "🏗",
    "Kema": "🚢",
    "Tog‘ lageri": "⛺️",
    # Russian
    "Ресторан": "🍽",
    "Самолет": "✈️",
    "Школа": "🏫",
    "Больница": "🏥",
    "Концерт": "🎤",
    "Космическая станция": "🚀",
    "Поезд": "🚆",
    "Пляж": "🏖",
    "Банк": "🏦",
    "Цирк": "🎪",
    "Отель": "🏨",
    "Супермаркет": "🛒",
    "Университет": "🎓",
    "Полицейский участок": "👮‍♂️",
    "Кинотеатр": "🎬",
    "Театр": "🎭",
    "Музей": "🏛",
    "Библиотека": "📚",
    "Стадион": "⚽️",
    "Зоопарк": "🦁",
    "Ферма": "🚜",
    "Стройплощадка": "🏗",
    "Корабль": "🚢",
    "Горный лагерь": "⛺️",
}


def get_locations(lang: str = "uz") -> dict[str, tuple[str, ...]]:
    return LOCATIONS_RU if lang == "ru" else LOCATIONS_UZ


def format_location(name: str) -> str:
    emoji = LOCATION_EMOJIS.get(name, "📍")
    return f"{emoji} {name}"

