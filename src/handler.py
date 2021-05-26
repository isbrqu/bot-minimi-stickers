from PIL import Image, ImageOps
from config import logger
from io import BytesIO
from slugify import slugify
from telegram import Update, Bot
from telegram.ext import CallbackContext
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
import config
import os

bot = Bot(config.token)

def transform_sticker(sticker):
    sticker_buffer = BytesIO(sticker)
    image = Image.open(sticker_buffer)
    image = ImageOps.scale(image, .5)
    size = (521, image.height)
    image = ImageOps.pad(image, size, centering=(0, 0))
    image_buffer = BytesIO()
    image.save(image_buffer, format='PNG')
    return image_buffer.getvalue()

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f'se ha inicia el bot')

def sticker(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = update.effective_message
    sticker_set = bot.get_sticker_set(msg.sticker.set_name)
    update.message.reply_text('descargando...')
    logger.info('download')
    with ThreadPoolExecutor(max_workers=2) as executor:
        stickers = executor.map(
            lambda sticker: sticker.get_file().download_as_bytearray(),
            sticker_set.stickers
        )
    update.message.reply_text('comprimiendo...')
    logger.info('compressing')
    zip_file_buffer = BytesIO()
    with ZipFile(zip_file_buffer, mode='w') as zip_file:
        for index, sticker in enumerate(stickers):
            image = transform_sticker(sticker)
            zip_file.writestr(f'{index}.png', image)
    logger.info('compressed')
    update.message.reply_text('comprimido')
    update.message.reply_text('upload...')
    zip_file_name = f'{slugify(sticker_set.name)}.zip'
    binary = zip_file_buffer.getvalue()
    update.message.reply_document(binary, zip_file_name, timeout=100)
    update.message.reply_text('se descargaron las imagenes las imagenes')

