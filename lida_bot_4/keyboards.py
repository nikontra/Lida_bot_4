from config import BUTTON1_LIST, BUTTON2_CLEAR
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup)


def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON1_LIST),
            KeyboardButton(BUTTON2_CLEAR),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def get_inline_keyboard_one_key(text: str, callback_data=None, url=None):
    """Клавиатура с одной кнопкой"""
    keyboard = (
        (
            InlineKeyboardButton(
                text=text, callback_data=callback_data, url=url
            ),
        ),
    )
    return InlineKeyboardMarkup(keyboard)
