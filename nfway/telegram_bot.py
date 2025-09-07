import logging
from tempfile import TemporaryFile
from traceback import print_exception

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from nfway import message_templates
from nfway.nf_info import NFInfo
from nfway.qrcode_reader import read_qrcode
from nfway.scrapper import read_url

# Enable logging
fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=fmt, level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def emitter_message(nf: NFInfo) -> str:
    return message_templates.EMITTER_HEADER_TEMPLATE.format(
        name=nf.emiter_name,
        cnpj=nf.emiter_cnpj,
        address=nf.emiter_address,
    )


def nf_info_message(nf: NFInfo) -> str:
    return message_templates.NF_INFO_TEMPLATE.format(
        number=nf.number,
        series=nf.series,
        access_key=nf.access_key,
        emission_date=nf.emission_date,
        emission_time=nf.emission_time,
    )


def list_items_message(nf: NFInfo) -> str:
    message = ""

    for item in nf.items:
        message += message_templates.ITEM_TEMPLATE.format(
            name=item.name,
            quantity=item.quantity,
            quantity_unit=item.quantity_unit,
            unit_value=item.unit_value,
            item_value=item.item_value,
        )

    message += message_templates.TOTAL_TEMPLATE.format(
        total_value=nf.total_value,
        total_taxes=nf.total_taxes,
    )

    return message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    welcome_message = f"Olá {user.first_name}. Seja bem vindo ao NF-Way."
    await update.message.reply_text(welcome_message)


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger.info(f"User {user.first_name} sent a link")

    try:
        nf_result = read_url(update.message.text)

    except Exception as e:
        print_exception(e)
        await update.message.reply_html(message_templates.BAD_URL_TEMPLATE)

    else:
        await update.message.reply_html(emitter_message(nf_result))
        if nf_result.emiter_coords is not None:
            await update.message.reply_location(
                latitude=nf_result.emiter_coords[0],
                longitude=nf_result.emiter_coords[1],
            )
        await update.message.reply_html(nf_info_message(nf_result))
        await update.message.reply_html(list_items_message(nf_result))


async def handle_qr_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger.info(f"User {user.first_name} sent an image")

    download_path = TemporaryFile().name
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(download_path)

    try:
        url = read_qrcode(download_path)

    except Exception as e:
        print_exception(e)
        await update.message.reply_html(message_templates.BAD_QR_CODE_TEMPLATE)
        return

    if url is None:
        await update.message.reply_html(message_templates.BAD_QR_CODE_TEMPLATE)
        return

    try:
        nf_result = read_url(url)

    except Exception as e:
        print_exception(e)
        await update.message.reply_html(message_templates.GOOD_QR_CODE_BAD_URL_TEMPLATE)

    else:
        await update.message.reply_html(emitter_message(nf_result))
        if nf_result.emiter_coords is not None:
            await update.message.reply_location(
                latitude=nf_result.emiter_coords[0],
                longitude=nf_result.emiter_coords[1],
            )
        await update.message.reply_html(nf_info_message(nf_result))
        await update.message.reply_html(list_items_message(nf_result))


async def default(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Envie um *QR code* ou o link de uma Nota Fiscal.")


def initialize(token: str) -> None:
    app = Application.builder().token(token).build()

    handlers = [
        CommandHandler("start", start),
        MessageHandler(
            filters.Entity("url") | filters.Entity("text_link"),
            handle_link,
        ),
        MessageHandler(filters.PHOTO, handle_qr_code),
        MessageHandler(filters.TEXT & ~filters.COMMAND, default),
    ]

    app.add_handlers(handlers)
    app.run_polling(allowed_updates=Update.ALL_TYPES)
