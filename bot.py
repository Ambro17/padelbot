import os
import textwrap

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from api import get_current_matches_as_string
import requests

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


@send_action(ChatAction.TYPING)
async def get_matches(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown_v2(
        f'```\n{get_current_matches_as_string()}\n```'
    )


@send_action(ChatAction.TYPING)
async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown_v2(
        textwrap.dedent(f"""\
        ```
        Jugador                 Pais Puntos \#
        Alejandro Galan         ESP  11950  1
        Juan Lebron             ESP  11950  1
        Arturo Coello           ESP  11760  3
        Martin Di Nenno         ARG  10665  4
        Franco Stupaczuk        ARG  9360   5
        Fernando Belasteguin    ARG  9230   6
        Francisco Navarro       ESP  9070   7
        Agustin Tapia           ARG  8030   8
        Federico Chingotto      ARG  7710   9
        Juan Tello              ARG  5670   10
        Pablo Lima              BRA  5495   11
        Carlos Daniel Gutierrez ARG  5140   12
        Alejandro Ruiz          ESP  4895   13
        Jeronimo Gonzalez       ESP  4505   14
        Luciano Capra           ARG  3308   15
        Maximiliano Sanchez     ARG  3308   15
        Victor Ruiz             ESP  3035   17
        Javier Garrido          ESP  2855   18
        Jorge Nieto             ESP  2790   19
        Lucas Bergamini         BRA  2755   20
        ```
        """)
    )


app = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("live", get_matches))
app.add_handler(CommandHandler("ranking", ranking))

print("The bot is running")
app.run_polling()