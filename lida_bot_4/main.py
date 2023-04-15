import logging

import config
import messages
from db import add_user, clear_user, init_db, list_user
from keyboards import get_base_reply_keyboard, get_inline_keyboard_one_key
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          ConversationHandler, InlineQueryHandler,
                          MessageHandler, filters)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


NAME, INFO, EMAIL, LESSON, GIFT = range(5)


async def do_list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Список пользователей оставивших контакты"""
    users = list_user()
    text = '\n'.join(
            [f'{username} - {email} - {id}' for username, email, id in users]
        )
    if text == '':
        text = 'Список контактов пуст'
    await update.effective_message.reply_text(
        text=text,
    )


async def do_clear_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очистить список контактов"""
    text = messages.MESSAGE_5
    await update.message.reply_text(
        text=text,
    ),


async def delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждает удаление списка контактов"""
    clear_user()
    text = 'Список контактов успешно очищен'
    await update.effective_message.reply_text(
        text=text,
    )


def do_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок админки"""
    text = update.message.text
    chat_id = update.effective_chat.id
    if text == config.BUTTON1_LIST and chat_id == config.OWNER_ID:
        return do_list_users(update=update, context=context)
    elif text == config.BUTTON2_CLEAR and chat_id == config.OWNER_ID:
        return do_clear_users(update=update, context=context)
    elif text == config.BUTTON3_CLEAR_CONFIRM and chat_id == config.OWNER_ID:
        return delete_confirm(update=update, context=context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Старт диалога, для Админа - админка"""
    chat_id: int = update.effective_chat.id
    if chat_id != config.OWNER_ID:
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.MESSAGE_1
        )
        return NAME

    await context.bot.send_message(
        chat_id=config.OWNER_ID,
        text='Привет',
        reply_markup=get_base_reply_keyboard()
    )


async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает имя пользователя"""
    context.user_data[NAME] = update.message.text
    text = f'{context.user_data[NAME]} {messages.MESSAGE_2}'
    await update.message.reply_text(text=text)
    return INFO


async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает информацию о пользователе"""
    text = messages.MESSAGE_3
    await update.message.reply_text(text=text)
    return EMAIL


async def email_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает почту пользователя"""
    context.user_data[EMAIL] = update.message.text
    add_user(
        username=context.user_data[NAME],
        email=context.user_data[EMAIL],
        chat_id=update.effective_chat.id
    )
    text = messages.MESSAGE_4
    await update.message.reply_text(
        text=text,
        reply_markup=get_inline_keyboard_one_key(
            text='Урок',
            url=config.URL1
        ),
    ),
    # job_time_message(
    #     context=context,
    #     chat_id=update.effective_chat.id,
    #     timer=1
    # )
    # return GIFT


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Отменить весь процесс диалога. Данные будут утеряны"""
    await update.message.reply_text('Отмена. Для начала с нуля нажмите /start')
    return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command."
    )


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=update.message.text
#     )


# async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text_caps = ' '.join(context.args).upper()
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=text_caps
#     )


# async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = []
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     await context.bot.answer_inline_query(update.inline_query.id, results)


# async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text="Sorry, I didn't understand that command."
#     )


def main():
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    init_db()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [
                MessageHandler(
                    filters.ALL, name_handler),
            ],
            INFO: [
                MessageHandler(
                    filters.ALL, info_handler),
            ],
            EMAIL: [
                MessageHandler(
                    filters.ALL, email_handler),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )

    message_handler = MessageHandler(filters.TEXT, do_echo)
    unknown_handler = MessageHandler(filters.TEXT, unknown)

    # caps_handler = CommandHandler('caps', caps)
    # inline_caps_handler = InlineQueryHandler(inline_caps)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(conv_handler)
    application.add_handler(message_handler)
    application.add_handler(unknown_handler)

    # application.add_handler(caps_handler)
    # application.add_handler(inline_caps_handler)
    # application.add_handler(echo_handler)
    # 

    application.run_polling()


if __name__ == '__main__':
    main()
