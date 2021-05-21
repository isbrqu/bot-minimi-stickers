import logging
import os
import random
import sys

from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

mode = os.getenv('MODE')
TOKEN = os.getenv('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')

if mode == 'dev':
    def run(updater):
        updater.start_polling()
elif mode == 'prod':
    def run(updater):
        url = f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}'
        updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
        updater.bot.set_webhook(url)
else:
    logger.error('No MODE specified!')
    sys.exit(1)

def start_handler(bot, update):
    id_ = update.effective_user['id']
    msg = 'Hello from Python!\nPress /random to get random number'
    logger.info(f'User {id_} started bot')
    update.message.reply_text(msg)

def random_handler(bot, update):
    id_ = update.effective_user['id']
    number = random.randint(0, 10)
    logger.info(f'User {id_} randomed number {number}')
    update.message.reply_text(f'Random number: {number}')

if __name__ == '__main__':
    logger.info('Starting bot')
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start_handler))
    updater.dispatcher.add_handler(CommandHandler('random', random_handler))
    run(updater)

