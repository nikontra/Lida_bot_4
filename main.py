import logging
import os

from dotenv import load_dotenv
from telegram import Bot, Update

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))


def main():
    pass


if __name__ == '__main__':
    main()
