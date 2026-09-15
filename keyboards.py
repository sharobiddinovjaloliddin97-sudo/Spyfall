from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from locations import format_location
from texts import tr


def lobby_keyboard(game, bot_username):
    keyboard = [
        [
            InlineKeyboardButton(
                tr("join_button"), callback_data=f"j:{game.sid}"
            ),
            InlineKeyboardButton(
                tr("leave_button"), callback_data=f"l:leave:{game.sid}"
            ),
        ]
    ]
    if len(game.players) >= 3:
        keyboard.append(
            [
                InlineKeyboardButton(
                    tr("start_button"), callback_data=f"l:start:{game.sid}"
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                tr("time_button", minutes=game.minutes),
                callback_data=f"l:time_menu:{game.sid}",
            ),
            InlineKeyboardButton(
                tr("how_to_button"),
                callback_data=f"l:rules:{game.sid}",
            ),
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                tr("open_bot"),
                url=f"https://t.me/{bot_username}?start=ready",
            )
        ]
    )
    return InlineKeyboardMarkup(keyboard)


def lobby_time_keyboard(game):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⏱ 5 daq", callback_data=f"l:time:{game.sid}:5"
                ),
                InlineKeyboardButton(
                    "⏱ 8 daq", callback_data=f"l:time:{game.sid}:8"
                ),
                InlineKeyboardButton(
                    "⏱ 10 daq", callback_data=f"l:time:{game.sid}:10"
                ),
                InlineKeyboardButton(
                    "⏱ 15 daq", callback_data=f"l:time:{game.sid}:15"
                ),
            ],
            [
                InlineKeyboardButton(
                    tr("back_button"), callback_data=f"l:back:{game.sid}"
                )
            ],
        ]
    )


def start_menu_keyboard(bot_username):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    tr("how_to_button"), callback_data="m:how"
                ),
                InlineKeyboardButton(
                    tr("tips_button"), callback_data="m:tips"
                ),
            ],
            [
                InlineKeyboardButton(
                    tr("locations_button"), callback_data="m:locs"
                )
            ],
            [
                InlineKeyboardButton(
                    tr("add_group_button"),
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
        ]
    )


def menu_back_keyboard(bot_username):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    tr("back_button"), callback_data="m:main"
                )
            ],
            [
                InlineKeyboardButton(
                    tr("add_group_button"),
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
        ]
    )


def spy_role_keyboard(chat_id, sid):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    tr("spy_locations_button"),
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
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    tr("yes"), callback_data=f"v:{game.sid}:1"
                ),
                InlineKeyboardButton(
                    tr("no"), callback_data=f"v:{game.sid}:0"
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

