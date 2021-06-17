import telebot
import os
from telebot import types

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


class InlineKeyboard:

    def to_search_page(message):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Сброс', callback_data='pay_search_main_page')
        keyboard.add(button)
        bot.send_message(message.chat.id, 'вернуться на главную', reply_markup=keyboard)

    def button_two_keyboard(message):
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Google',  # текст на кнопке
            url='https://google.com'
        )
        keyboard.add(url_button)
        bot.send_message(message.chat.id,
                         'If you press the button then go to google',
                         reply_markup=keyboard
                         )

    def callback_keyboard(message, buttons: dict, msg):
        keyboard = types.InlineKeyboardMarkup()

        for k, v in buttons.items():
            button = types.InlineKeyboardButton(text=v,
                                                callback_data=k)  # Параметр который вы передаете через callback заполняется в отдельный словарь который вам отправляет сервер. Оно не пишется в чат телеграма.

            keyboard.add(button)

        bot.send_message(message.chat.id, msg, reply_markup=keyboard, parse_mode='html')

    def callback_keyboard_one_row(message, buttons: dict, msg):

        arr_btn = []
        for k, v in buttons.items():
            btn = types.InlineKeyboardButton(text=v, callback_data=k)
            arr_btn.append(btn)

        key = []
        for bt in arr_btn:
            key.append(bt)

        to_main_btn = [types.InlineKeyboardButton(text=u'\U00002B05' + ' На главную', callback_data='start')]
        keyboard = [] + [key] + [to_main_btn]

        reply_markup = types.InlineKeyboardMarkup(keyboard)

        # bot.send_message(message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
        bot.edit_message_text(msg, message.chat.id, message.id, parse_mode='html', reply_markup=reply_markup)

    def callback_keyboard_one_row_only_button(message, buttons: dict, msg):

        arr_btn = []
        for k, v in buttons.items():
            btn = types.InlineKeyboardButton(text=v, callback_data=k)
            arr_btn.append(btn)

        key = []
        for bt in arr_btn:
            key.append(bt)

        keyboard = [] + [key]

        reply_markup = types.InlineKeyboardMarkup(keyboard)

        # bot.send_message(message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
        bot.edit_message_text(msg, message.chat.id, message.id, parse_mode='html', reply_markup=reply_markup)


def init_nav_button():
    keyboard = [
        [
            types.InlineKeyboardButton(u'\U00002B05' + ' На главную', callback_data='start'),
            types.InlineKeyboardButton(u'\U0000267B' + ' Сброс', callback_data='pay_search_main_page'),
        ]
    ]

    return types.InlineKeyboardMarkup(keyboard)


def init_nav_button_pay():
    keyboard = [
        [types.InlineKeyboardButton('Оформить подписку', pay=True)],
        [types.InlineKeyboardButton(u'\U00002B05' + ' На главную', callback_data='start')]
    ]

    return types.InlineKeyboardMarkup(keyboard)