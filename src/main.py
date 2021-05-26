from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    Updater
)
import config
import handler
import sys

if __name__ == '__main__':
    config.logger.info('Starting bot')
    updater = Updater(config.token)
    updater.dispatcher.add_handler(CommandHandler('start', handler.start))
    updater.dispatcher.add_handler(MessageHandler(Filters.sticker, handler.sticker))
    if config.mode == 'dev':
        config.logger.info('mode dev')
        updater.start_polling(timeout=100)
    elif config.mode == 'prod':
        config.logger.info('mode prod')
        updater.start_webhook(**config.webhook)
    else:
        config.logger.error('No MODE specified!')
        sys.exit(1)

