import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))


BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_FILE = BASE_DIR / "db.sqlite3"


BUTTON1_LIST = 'Список контактов'
BUTTON2_CLEAR = 'Очистить список'
BUTTON3_CLEAR_CONFIRM = 'Подтверждаю удаление'

CALLBACK_BUTTON1_LESSON1 = "callback_button1_lesson1"

TITLES = {
    CALLBACK_BUTTON1_LESSON1: "Посмотреть урок",
}

URL1 = 'https://clck.ru/32DUSp'
