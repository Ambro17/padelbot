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
    await update.message.reply_text(textwrap.dedent(f"""\
     Hola, soy un bot al que le gusta el padel 
     Podés escribir /live para ver los resultados de los partidos en curso
     /horarios para ver los horarios de los partidos de hoy y
     /ranking para conocer el ranking de Premier Padel
     """))


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
        Arturo Coello 			ESP  12910  1
        Alejandro Galan 		ESP  12200  2
        Juan Lebron 			ESP  12200  2
        Martin Di Nenno 		ARG  10455  4
        Francisco Navarro 		ESP  9970   5
        Agustin Tapia 			ARG  9730   6
        Franco Stupaczuk 		ARG  8950   7
        Fernando Belasteguin 	ARG  8740   8
        Federico Chingotto 		ARG  8610   9
        Juan Tello 				ARG  5550   10
        Pablo Lima 				BRA  5345   11
        Carlos Daniel Gutierrez ARG  5020   12
        Alejandro Ruiz 			ESP  4565   13
        Jeronimo Gonzalez 		ESP  4175   14
        Luciano Capra 			ARG  3498   15
        Maximiliano Sanchez 	ARG  3498   15
        Jorge Nieto 			ESP  3455   17
        Victor Ruiz 			ESP  3350   18
        Lucas Bergamini 		BRA  3070   19
        Javier Garrido 			ESP  2950   20
        ```
        """)
    )


@send_action(ChatAction.TYPING)
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('El proximo torneo Premier Padel comienza el 30 de Octubre en Egipto\nhttps://www.padelfip.com/events/newgiza-premier-padel-p1-2023/')


app = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("live", get_matches))
app.add_handler(CommandHandler("ranking", ranking))
app.add_handler(CommandHandler("horarios", today))

print("The bot is running")
app.run_polling()