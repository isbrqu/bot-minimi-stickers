from os import getenv as env
import logging

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
mode = env('MODE')
token = env('TOKEN')
app_name = env('APP_NAME')
webhook = {
    'listen': env('LISTEN'),
    'port': env('PORT'),
    'url_path': env('TOKEN'),
    'webhook_url': f'https://{app_name}.herokuapp.com/{token}'
}

logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger()

