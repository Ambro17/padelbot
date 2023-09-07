import os

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from api import get_current_matches_as_string

from functools import wraps


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context, *args, **kwargs)

        return command_func

    return decorator


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hola, tipeá /live y te contestaré con los partidos en curso')


@send_action(ChatAction.TYPING)
async def get_matches(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown_v2(
        f'```\n{get_current_matches_as_string()}\n```'
    )


app = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("live", get_matches))

print("The bot is running")
app.run_polling()