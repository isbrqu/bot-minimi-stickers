from io import BytesIO
from PIL import Image, ImageOps
from telegram import Update, Bot
from telegram.ext import CallbackContext
from config import logger
import config
import os

bot = Bot(config.token)

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f'se ha inicia el bot')

def sticker(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = update.effective_message
    sticker_set = bot.get_sticker_set(msg.sticker.set_name)
    folder = f'img/{user.id}/{sticker_set.name}'
    os.makedirs(folder, exist_ok=True)
    update.message.reply_text('descargando imagenes...')
    for index, sticker in enumerate(sticker_set.stickers):
        sticker_file = sticker.get_file().download_as_bytearray()
        image = Image.open(BytesIO(sticker_file))
        image = ImageOps.scale(image, .5)
        _, y = image.size
        image = ImageOps.pad(image, size=(512, y), centering=(0, 0))
        image.save(f'{folder}/{index}.png')
    update.message.reply_text('se descargaron las imagenes las imagenes')

