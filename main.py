import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import (
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
)
from telegram.error import TelegramError
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
)

from handlers import game, lobby, voting
from service import GameService
from storage import MemoryStorage
from texts import tr


async def post_init(application):
    private_commands = [
        BotCommand("start", "Bosh menyu / Главное меню"),
        BotCommand("help", "Qoidalar / Правила"),
        BotCommand("locations", "Joylar / Локации"),
        BotCommand("lang", "Til / Язык"),
    ]
    group_commands = [
        BotCommand("newgame", "Yangi o‘yin / Новая игра"),
        BotCommand("help", "Qoidalar / Правила"),
        BotCommand("locations", "Joylar / Локации"),
        BotCommand("players", "Ishtirokchilar / Игроки"),
        BotCommand("accuse", "Ayblash / Обвинить"),
        BotCommand("stats", "Statistika / Статистика"),
        BotCommand("lang", "Til / Язык"),
        BotCommand("endgame", "O‘yinni to‘xtatish / Остановить"),
    ]
    try:
        await application.bot.set_my_commands(
            private_commands, scope=BotCommandScopeAllPrivateChats()
        )
        await application.bot.set_my_commands(
            group_commands, scope=BotCommandScopeAllGroupChats()
        )
    except Exception as exc:
        logging.warning("Telegram menyusini o‘rnatib bo‘lmadi: %s", exc)


async def error_handler(update, context):
    logging.error("Xatolik turi: %s", type(context.error).__name__)

    if update and update.effective_chat:
        service = context.application.bot_data["service"]
        await service.send(update.effective_chat.id, tr("error"))


def build_application(token):
    application = (
        ApplicationBuilder()
        .token(token)
        .concurrent_updates(32)
        .connection_pool_size(64)
        .pool_timeout(30)
        .post_init(post_init)
        .build()
    )

    application.bot_data["service"] = GameService(
        application,
        MemoryStorage(),
    )

    commands = {
        "start": game.start,
        "help": game.help_command,
        "newgame": lobby.newgame,
        "join": lobby.join,
        "leave": lobby.leave,
        "players": lobby.players,
        "settime": lobby.settime,
        "startgame": game.startgame,
        "endgame": game.endgame,
        "accuse": voting.accuse,
        "stats": game.stats,
        "locations": game.locations,
        "lang": game.lang_command,
        "language": game.lang_command,
    }

    for command, handler in commands.items():
        application.add_handler(CommandHandler(command, handler))

    application.add_handler(CallbackQueryHandler(voting.callback))
    application.add_error_handler(error_handler)

    return application


def main():
    load_dotenv(Path(__file__).resolve().parent / ".env")
    token = os.getenv("BOT_TOKEN", "").strip()

    if not token or token == "your_token_here":
        raise SystemExit(tr("token_missing"))

    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    print(tr("running"))

    try:
        application = build_application(token)
        application.run_polling(
            allowed_updates=["message", "callback_query"],
        )
    except (TelegramError, ValueError):
        raise SystemExit(tr("startup_error")) from None


if __name__ == "__main__":
    main()