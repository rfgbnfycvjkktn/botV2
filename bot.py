# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption

import users
import messages
from keyboards import InlineKeyboard
import bonds
import keyboards

import os
import re
import prettytable as pt
import datetime

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# платежи
provider_token = os.getenv("TELEGRAM_PROVIDER_TOKEN")
prices = [LabeledPrice(label='Подписка', amount=30000)]

param = {'yieldless': 0, 'yieldmore': 0, 'priceless': 0, 'pricemore': 0, 'durationless': 0, 'durationmore': 0,
         'volume': 0}  # параметры запроса


# стартовая страница обработка команды
@bot.message_handler(commands=["start"])
def start_command(message):
    bot.clear_step_handler(message)
    buttons = {'search_main_page': u'\U0001F50D' + ' Поиск', 'buy': u'\U0001F4B3' + ' Подписка',
               'help': u'\U00002139' + ' Помощь'}
    InlineKeyboard.callback_keyboard(message, buttons, messages.start_menu())

    user = users.User()
    data = {'id': message.from_user.id,
            'name': message.from_user.first_name,
            'username': message.from_user.username,
            'email': "",
            'access': False,
            'reg_date': datetime.datetime.today().replace(microsecond=0),
            'sub_start_date': None,
            'sub_end_date': None}
    user.add(data)


# стартовая страница через callback
@bot.callback_query_handler(func=lambda query: query.data == 'start')
def callback_inline(call):
    bot.clear_step_handler(call.message)
    buttons = {'search_main_page': u'\U0001F50D' + ' Поиск', 'buy': u'\U0001F4B3' + ' Подписка',
               'help': u'\U00002139' + ' Помощь'}
    InlineKeyboard.callback_keyboard(call.message, buttons, messages.start_menu())

    user = users.User()
    data = {'id': call.from_user.id,
            'name': call.from_user.first_name,
            'username': call.from_user.username,
            'email': "",
            'access': False,
            'reg_date': datetime.datetime.today().replace(microsecond=0),
            'sub_start_date': None,
            'sub_end_date': None}
    user.add(data)


# страница помощи обработка команды
@bot.message_handler(commands=["help"])
def start_command(call):
    buttons = {'start': u'\U00002B05' + ' На главную'}
    InlineKeyboard.callback_keyboard(call, buttons, messages.help_menu())


# страница помощи
@bot.callback_query_handler(func=lambda query: query.data == 'help')
def callback_inline(call):
    buttons = {'start': u'\U00002B05' + ' На главную'}
    InlineKeyboard.callback_keyboard(call.message, buttons, messages.help_menu())


# статус подписки
@bot.message_handler(commands=["sub"])
def start_command(call):
    user = users.User()
    data = call.from_user.id

    status = user.check_sub(data)
    if status["status_sub"]:
        buttons = {'start': u'\U00002B05' + ' На главную'}
        # date_obj = datetime.datetime.strptime(status["sub_end"], '%Y-%m-%d')

        # InlineKeyboard.callback_keyboard(call, buttons, "Подписка активна до: " + date_obj.strftime("%d") + "." + date_obj.strftime("%m") + "." + date_obj.strftime("%Y"))
        InlineKeyboard.callback_keyboard(call, buttons,
                                         "Подписка активна до: " + status['sub_end'].strftime("%d.%m.%Y"))
    else:
        buttons = {'start': u'\U00002B05' + ' На главную'}
        InlineKeyboard.callback_keyboard(call, buttons, "Подписка не активирована!")


@bot.callback_query_handler(func=lambda query: query.data == 'search_main_page')
def callback_inline(call):
    buttons = {'free_search_main_page': u'\U0001F50D' + ' Поиск (бесплатно)',
               'pay_search_main_page': u'\U0001F50D' + ' Поиск (по подписке)',
               'start': u'\U00002B05' + ' На главную'}

    InlineKeyboard.callback_keyboard(call.message, buttons, messages.search_menu())


# поиск по бесплатному тарифу
@bot.callback_query_handler(func=lambda query: query.data == 'free_search_main_page')
def callback_inline(call):
    # buttons = {'yield_less_4': '4', 'yield_less_5': '5', 'yield_less_6': '6', 'yield_less_7': '7'}
    buttons = {'yield_less_5': '5', 'yield_less_6': '6', 'yield_less_7': '7'}
    InlineKeyboard.callback_keyboard_one_row(call.message, buttons, 'Доходность от (%):')


# поиск по платному тарифу
@bot.callback_query_handler(func=lambda query: query.data == 'pay_search_main_page')
def callback_inline(message):
    user = users.User()
    data = message.from_user.id

    if user.paid(data):
        bot.clear_step_handler(message.message)

        reply_markup = keyboards.init_nav_button()

        msg = bot.send_message(message.message.chat.id, 'Доходность от (%):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_yield_less_step)
    else:
        buttons = {'start': u'\U00002B05' + ' На главную'}
        InlineKeyboard.callback_keyboard(message.message, buttons, "Подписка не активирована! Поиск невозможен.")


@bot.message_handler(commands=["buy"])
def start_command(call):

    bot.clear_step_handler(call)

    reply_markup = keyboards.init_nav_button_pay()

    bot.send_invoice(call.chat.id, title='Подписка (30 дней)',
                     description=' Подписка открывает доступ к расширенному поиску облигаций на 30 дней с даты оплаты.',
                     provider_token=provider_token,
                     currency='RUB',
                     photo_url='',
                     photo_height=None,  # !=0/None or picture won't be shown
                     photo_width=None,
                     photo_size=None,
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     prices=prices,
                     start_parameter='subs',
                     invoice_payload='Subscribe 30',
                     reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda query: query.data == 'buy')
def callback_inline(call):
    bot.clear_step_handler(call.message)

    reply_markup = keyboards.init_nav_button_pay()

    bot.send_invoice(call.message.chat.id, title='Подписка (30 дней)',
                     description=' Подписка открывает доступ к расширенному поиску облигаций на 30 дней с даты оплаты.',
                     provider_token=provider_token,
                     currency='RUB',
                     photo_url='',
                     photo_height=None,  # !=0/None or picture won't be shown
                     photo_width=None,
                     photo_size=None,
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     prices=prices,
                     start_parameter='subs',
                     invoice_payload='Subscribe 30',
                     reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda c: True)
def callback_inline(callback):
    if re.match('yield_less_', callback.data):
        # print("Выбрана доходность от")
        yieldless = callback.data.replace('yield_less_', "")
        param['yieldless'] = float(yieldless)

        # кнопки следующего меню
        # buttons = {'yield_more_5': '5', 'yield_more_6': '6', 'yield_more_7': '7', 'yield_more_8': '8'}
        buttons = {'yield_more_6': '6', 'yield_more_7': '7', 'yield_more_8': '8'}
        InlineKeyboard.callback_keyboard_one_row(callback.message, buttons, 'Доходность до (%):')

    elif re.match('yield_more_', callback.data):
        # print("Выбрана доходность до")
        yieldmore = callback.data.replace('yield_more_', "")
        param['yieldmore'] = float(yieldmore)

        # кнопки следующего меню
        buttons = {'price_less_98': '98', 'price_less_99': '99'}
        InlineKeyboard.callback_keyboard_one_row(callback.message, buttons, 'Цена от (% от номинала):')

    elif re.match('price_less_', callback.data):
        # print("Выбрана цена от")
        priceless = callback.data.replace('price_less_', "")
        param['priceless'] = float(priceless)

        # кнопки следующего меню
        buttons = {'price_more_99': '99', 'price_more_100': '100'}
        InlineKeyboard.callback_keyboard_one_row(callback.message, buttons, 'Цена до (% от номинала):')

    elif re.match('price_more_', callback.data):
        # print("Выбрана цена до")
        pricemore = callback.data.replace('price_more_', "")
        param['pricemore'] = float(pricemore)

        # все параметры бесплатного тарифа выбраны/установлены. Нужно произвести расчет
        param['volume'] = 3000

        param['durationless'] = 8
        param['durationmore'] = 24

        bot.send_chat_action(callback.message.chat.id, 'typing', 10)

        buttons = {}
        InlineKeyboard.callback_keyboard_one_row(callback.message, buttons,
                                                 '<b>Параметры поиска:</b> \n' + 'Доходность от ' + str(
                                                     param['yieldless']) + ' до ' + str(
                                                     param['yieldmore']) + '\n' + 'Цена от ' + str(
                                                     param['priceless']) + ' до ' + str(
                                                     param['pricemore']) + '\n' + 'Дюрация от ' + str(
                                                     param['durationless']) + ' до ' + str(
                                                     param['durationmore']) + '\n' + 'Объем торгов от ' + str(
                                                     param['volume']) + '\n\n' + ' Идёт поиск ...')
        print(param)
        start_request(callback.message, False)


# обработчики платного поиска +++
def process_yield_less_step(message):
    reply_markup = keyboards.init_nav_button()

    try:
        param['yieldless'] = float(message.text)
        msg = bot.reply_to(message, 'Доходность до (%):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_yield_more_step)

    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_yield_more_step(message):
    reply_markup = keyboards.init_nav_button()

    try:
        param['yieldmore'] = float(message.text)
        msg = bot.reply_to(message, 'Цена от (% от номинала):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_price_less_step)

    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_price_less_step(message):
    reply_markup = keyboards.init_nav_button()

    try:
        param['priceless'] = float(message.text)

        reply_markup = keyboards.init_nav_button()
        msg = bot.reply_to(message, 'Цена до (% от номинала):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_price_more_step)

    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_price_more_step(message):
    reply_markup = keyboards.init_nav_button()

    try:
        param['pricemore'] = float(message.text)
        msg = bot.reply_to(message, 'Дюрация от (мес.):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_duration_less_step)

    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_duration_less_step(message):
    reply_markup = keyboards.init_nav_button()

    try:
        param['durationless'] = float(message.text)
        msg = bot.reply_to(message, 'Дюрация до (мес.):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_duration_more_step)

    except Exception as e:

        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_duration_more_step(message):
    reply_markup = keyboards.init_nav_button()

    try:
        param['durationmore'] = float(message.text)
        msg = bot.reply_to(message, 'Объём торгов от (шт.):', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, process_volume_step)

    except Exception as e:
        bot.reply_to(message, u'\U000026D4' + ' ошибочный ввод', reply_markup=reply_markup)


def process_volume_step(message):
    param['volume'] = int(message.text)

    bot.clear_step_handler(message)

    bot.send_message(message.chat.id,
                     '<b>Параметры поиска:</b> \n'
                     + 'Доходность от ' + str(param['yieldless']) + ' до ' + str(param['yieldmore'])
                     + '\n' + 'Цена от ' + str(param['priceless']) + ' до ' + str(param['pricemore'])
                     + '\n' + 'Дюрация от ' + str(param['durationless']) + ' до ' + str(param['durationmore'])
                     + '\n' + 'Объем торгов от ' + str(param['volume'])
                     + '\n\n' + ' Идёт поиск ...', parse_mode='html')

    start_request(message, True)


def start_request(message, paid=False):
    out_result = bonds.get_bonds(param)
    # получили данные

    if paid:
        table = pt.PrettyTable(['ИД', 'Наименование', 'Цена', 'Доход', 'Объём', 'Д-я'])
        table.align['Д-я'] = 'c'
    else:
        table = pt.PrettyTable(['ИД', 'Наименование', 'Цена', 'Доход', 'Объём'])

    table.align['ИД'] = 'l'
    table.align['Наименование'] = 'l'
    table.align['Цена'] = 'c'
    table.align['Доход'] = 'c'
    table.align['Объём'] = 'c'

    for bond in out_result:
        name = bond[1][0:20]
        if paid:
            table.add_row([bond[0], name, bond[2], bond[3], bond[4], bond[5]])
        else:
            table.add_row([bond[0], name, bond[2], bond[3], bond[4]])

    buttons = {'start': u'\U00002B05' + ' На главную'}
    InlineKeyboard.callback_keyboard(message, buttons, '<b>Результаты поиска</b> \n' + f'<pre>{table}</pre>')
# обработчики платного поиска ---


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Произошла ошибка во время оплаты. Попробуйте произвести операцию позже.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Платеж {} {} потвержден.'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')

    user = users.User()
    sub_end_date = datetime.datetime.today().replace(microsecond=0) + datetime.timedelta(days=30)
    data = {'id': message.from_user.id,
            'name': message.from_user.first_name,
            'email': "",
            'username': message.from_user.username,
            'access': True,
            'reg_date': datetime.datetime.today().replace(microsecond=0),
            'sub_start_date': datetime.datetime.today().replace(microsecond=0),
            'sub_end_date': sub_end_date}
    user.add_sub(data)

    buttons = {'start': u'\U00002B05' + ' На главную'}
    InlineKeyboard.callback_keyboard(message, buttons, "Подписка активирована до: " + sub_end_date.strftime("%d.%m.%Y"))


bot.polling()
