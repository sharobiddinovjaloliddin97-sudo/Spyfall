from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from locations import format_location
from texts import tr


def lobby_keyboard(game, bot_username):
    lang = getattr(game, "lang", "uz")
    keyboard = [
        [
            InlineKeyboardButton(
                tr("join_button", lang=lang), callback_data=f"j:{game.sid}"
            ),
            InlineKeyboardButton(
                tr("leave_button", lang=lang),
                callback_data=f"l:leave:{game.sid}",
            ),
        ]
    ]
    if len(game.players) >= 3:
        keyboard.append(
            [
                InlineKeyboardButton(
                    tr("start_button", lang=lang),
                    callback_data=f"l:start:{game.sid}",
                )
            ]
        )
    current_lang_label = "🇺🇿 O‘zbek" if lang == "uz" else "🇷🇺 Русский"
    keyboard.append(
        [
            InlineKeyboardButton(
                tr("time_button", lang=lang, minutes=game.minutes),
                callback_data=f"l:time_menu:{game.sid}",
            ),
            InlineKeyboardButton(
                f"🌐 {current_lang_label}",
                callback_data=f"l:lang_menu:{game.sid}",
            ),
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                tr("how_to_button", lang=lang),
                callback_data=f"l:rules:{game.sid}",
            ),
            InlineKeyboardButton(
                tr("open_bot", lang=lang),
                url=f"https://t.me/{bot_username}?start=ready",
            ),
        ]
    )
    return InlineKeyboardMarkup(keyboard)


def lobby_time_keyboard(game):
    lang = getattr(game, "lang", "uz")
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⏱ 5 " + ("daq" if lang == "uz" else "мин"),
                    callback_data=f"l:time:{game.sid}:5",
                ),
                InlineKeyboardButton(
                    "⏱ 8 " + ("daq" if lang == "uz" else "мин"),
                    callback_data=f"l:time:{game.sid}:8",
                ),
                InlineKeyboardButton(
                    "⏱ 10 " + ("daq" if lang == "uz" else "мин"),
                    callback_data=f"l:time:{game.sid}:10",
                ),
                InlineKeyboardButton(
                    "⏱ 15 " + ("daq" if lang == "uz" else "мин"),
                    callback_data=f"l:time:{game.sid}:15",
                ),
            ],
            [
                InlineKeyboardButton(
                    tr("back_button", lang=lang),
                    callback_data=f"l:back:{game.sid}",
                )
            ],
        ]
    )


def lobby_lang_keyboard(game):
    lang = getattr(game, "lang", "uz")
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🇺🇿 O‘zbekcha",
                    callback_data=f"l:set_lang:{game.sid}:uz",
                ),
                InlineKeyboardButton(
                    "🇷🇺 Русский",
                    callback_data=f"l:set_lang:{game.sid}:ru",
                ),
            ],
            [
                InlineKeyboardButton(
                    tr("back_button", lang=lang),
                    callback_data=f"l:back:{game.sid}",
                )
            ],
        ]
    )


def start_menu_keyboard(bot_username, lang="uz"):
    current_lang_label = "🇺🇿 O‘zbekcha" if lang == "uz" else "🇷🇺 Русский"
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    tr("how_to_button", lang=lang), callback_data="m:how"
                ),
                InlineKeyboardButton(
                    tr("tips_button", lang=lang), callback_data="m:tips"
                ),
            ],
            [
                InlineKeyboardButton(
                    tr("locations_button", lang=lang), callback_data="m:locs"
                ),
                InlineKeyboardButton(
                    f"🌐 {current_lang_label}",
                    callback_data="m:lang_menu",
                ),
            ],
            [
                InlineKeyboardButton(
                    tr("add_group_button", lang=lang),
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
        ]
    )


def menu_lang_keyboard(bot_username, lang="uz"):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🇺🇿 O‘zbekcha", callback_data="m:set_lang:uz"
                ),
                InlineKeyboardButton(
                    "🇷🇺 Русский", callback_data="m:set_lang:ru"
                ),
            ],
            [
                InlineKeyboardButton(
                    tr("back_button", lang=lang), callback_data="m:main"
                )
            ],
        ]
    )


def menu_back_keyboard(bot_username, lang="uz"):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    tr("back_button", lang=lang), callback_data="m:main"
                )
            ],
            [
                InlineKeyboardButton(
                    tr("add_group_button", lang=lang),
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
        ]
    )


def spy_role_keyboard(chat_id, sid, lang="uz"):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    tr("spy_locations_button", lang=lang),
                    callback_data=f"s:locs:{chat_id}:{sid}",
                )
            ]
        ]
    )


def accuse_keyboard(game, accuser_id):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    player.name[:50],
                    callback_data=f"a:{game.sid}:{uid}",
                )
            ]
            for uid, player in game.players.items()
            if uid != accuser_id
        ]
    )


def vote_keyboard(game):
    lang = getattr(game, "lang", "uz")
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    tr("yes", lang=lang), callback_data=f"v:{game.sid}:1"
                ),
                InlineKeyboardButton(
                    tr("no", lang=lang), callback_data=f"v:{game.sid}:0"
                ),
            ]
        ]
    )


def guess_keyboard(game):
    buttons = [
        InlineKeyboardButton(
            format_location(name),
            callback_data=f"g:{game.chat_id}:{game.sid}:{index}",
        )
        for index, name in enumerate(game.locations)
    ]
    return InlineKeyboardMarkup(
        [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    )


