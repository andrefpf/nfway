import logging
from traceback import print_exception

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from tempfile import TemporaryFile

from nfway.scrapper import read_url
from nfway.qrcode_reader import read_qrcode

# Enable logging
fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=fmt, level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    welcome_message = f"Olá {user.first_name}. Seja bem vindo ao NF-Way."
    await update.message.reply_text(welcome_message)


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger.info(f"User {user.first_name} sent a link")

    try:
        result_value = read_url(update.message.text)
    except Exception as e:
        print_exception(e)

        response_text = "Não foi possível ler a Nota Fiscal.\n"
        response_text += "Verifique se o link informado pertence ao site oficial: https://sat.sef.sc.gov.br/."
        await update.message.reply_text(response_text)
    else:
        await update.message.reply_text(str(result_value))


async def handle_qr_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger.info(f"User {user.first_name} sent an image")

    download_path = TemporaryFile().name
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(download_path)

    url = read_qrcode(download_path)
    if url is None:
        response_text = "Não foi possível identificar o QR code informado.\n"
        response_text += "Por favor, tente novamente com uma imagem mais nítida."
        await update.message.reply_text(response_text)
        return

    try:
        result_value = read_url(url)
    except Exception as e:
        print_exception(e)

        response_text = "O correto QR code foi identificado, mas nao foi possivel ler a Nota Fiscal."
        await update.message.reply_text(response_text)
    else:
        await update.message.reply_text(str(result_value))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Envie um QR code ou o link de uma Nota Fiscal.")


def initialize(token: str) -> None:
    app = Application.builder().token(token).build()

    handlers = [
        CommandHandler("start", start),
        MessageHandler(
            filters.Entity("url") | filters.Entity("text_link"), handle_link
        ),
        MessageHandler(filters.PHOTO, handle_qr_code),
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo),
    ]

    app.add_handlers(handlers)
    app.run_polling(allowed_updates=Update.ALL_TYPES)
