from PIL import Image, ImageOps
from config import logger
from io import BytesIO
from slugify import slugify
from telegram import Update, Bot
from telegram.ext import CallbackContext
from zipfile import ZipFile
import config
import os

bot = Bot(config.token)

def transform_sticker(sticker):
    sticker_bytes = sticker.get_file().download_as_bytearray()
    sticker_buffer = BytesIO(sticker_bytes)
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
    zip_file_buffer = BytesIO()
    update.message.reply_text('descargando imagenes...')
    with ZipFile(zip_file_buffer, mode='w') as zip_file:
        for index, sticker in enumerate(sticker_set.stickers):
            logger.info(f'descargando: {index}.webp')
            image = transform_sticker(sticker)
            logger.info(f'guardando')
            zip_file.writestr(f'{index}.png', image)
    zip_file_name = f'{slugify(sticker_set.name)}.zip'
    update.message.reply_document(zip_file_buffer.getvalue(), zip_file_name)
    update.message.reply_text('se descargaron las imagenes las imagenes')

