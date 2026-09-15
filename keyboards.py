from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from texts import tr


def lobby_keyboard(game, bot_username):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    tr("join_button"),
                    callback_data=f"j:{game.sid}",
                )
            ],
            [
                InlineKeyboardButton(
                    tr("open_bot"),
                    url=f"https://t.me/{bot_username}?start=ready",
                )
            ],
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
            name,
            callback_data=f"g:{game.chat_id}:{game.sid}:{index}",
        )
        for index, name in enumerate(game.locations)
    ]
    return InlineKeyboardMarkup(
        [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    )
