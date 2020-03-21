import telebot
from telebot import types
import shelve
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv
import os

bot = telebot.TeleBot('TOKEN')
# user_id = 0
id_for_all = 0
dict_cost_type = dict()
dict_cost_type['now'] = 0
dict_cost_type['products'] = 0
dict_cost_type['eating_out'] = 0
dict_cost_type['transport'] = 0
dict_cost_type['purchases'] = 0
dict_cost_type['home'] = 0
dict_cost_type['entertainment'] = 0
dict_cost_type['services'] = 0
dict_cost_type['all'] = 0

cost = 0

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True, True, True)
keyboard1.row('/add', '/show', '/graph')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Выбери действие', reply_markup=keyboard1)
    # bot.register_next_step_handler(message, add_new)


@bot.message_handler(commands=['add'])
def add_new(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, types_cost)
    # elif message.text.lower() == 'Показать по категориям':
    # elif message.text.lower() == 'График':


@bot.message_handler(commands=['show'])
def show(message):
    bot.send_message(message.chat.id, '*Ваши расходы*', parse_mode='MARKDOWN')
    user_id = message.from_user.id
    first_db(user_id)
    open_db(user_id)
    # pr_products = round(((dict_cost_type['products']/dict_cost_type['all'])*100), 2)
    s1 = 'Потрачено всего:  {0:30}\n'.format(str(dict_cost_type['all']))
    s2 = '`{:15}|{:8}|{:6}`\n'.format('Продукты', str(dict_cost_type['products']), proc('products'))
    s3 = '`{:15}|{:8}|{:6}`\n'.format('Еда вне дома', str(dict_cost_type['eating_out']), proc('eating_out'))
    s4 = '`{:15}|{:8}|{:6}`\n'.format('Транспорт', str(dict_cost_type['transport']), proc('transport'))
    s5 = '`{:15}|{:8}|{:6}`\n'.format('Покупки', str(dict_cost_type['purchases']), proc('purchases'))
    s6 = '`{:15}|{:8}|{:6}`\n'.format('Дом. хоз-во', str(dict_cost_type['home']), proc('home'))
    s7 = '`{:15}|{:8}|{:6}`\n'.format('Развлечения', str(dict_cost_type['entertainment']), proc('entertainment'))
    s8 = '`{:15}|{:8}|{:6}`\n'.format('Услуги', str(dict_cost_type['services']), proc('services'))
    bot.send_message(message.chat.id, s1+ s2 + s3 + s4 + s5 + s6 + s7 + s8, parse_mode='MARKDOWN')


@bot.message_handler(commands=['graph'])
def add_new(message):
    bot.send_message(message.chat.id, '*Круговая диаграмма*', parse_mode='MARKDOWN')
    user_id = message.from_user.id
    open_db(user_id)

    data_names = ['Продукты', 'Еда вне дома', 'Транспорт', 'Покупки',
                  'Дом. хоз-о', 'Развлечения', 'Услуги']
    data_values = [dict_cost_type['products'], dict_cost_type['eating_out'], dict_cost_type['transport'],
                   dict_cost_type['purchases'], dict_cost_type['home'],
                   dict_cost_type['entertainment'], dict_cost_type['services']]

    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})

    plt.title('Ваши расходы(%)')

    xs = range(len(data_names))

    plt.pie(
        data_values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(data_names) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=data_names)
    fig.savefig('pie.png')
    bot.send_photo(message.chat.id, open('pie.png', 'rb'))


def proc(type_):
    if dict_cost_type['all'] == 0:
        return 0
    pr = str(round(((dict_cost_type[type_] / dict_cost_type['all']) * 100), 2))
    return pr + '%'


def first_db(user_id):
    # file_name = str(user_id)
    # db = shelve.open(file_name)
    directory = './'
    files = os.listdir(directory)
    fl = (str(user_id) + '.dat') in files
    if fl != True:
        # dict_cost_type['now'] = 0
        # dict_cost_type['products'] = 0
        # dict_cost_type['eating_out'] = 0
        # dict_cost_type['transport'] = 0
        # dict_cost_type['purchases'] = 0
        # dict_cost_type['home'] = 0
        # dict_cost_type['entertainment'] = 0
        # dict_cost_type['services'] = 0
        # dict_cost_type['all'] = 0
        save_db(user_id)



def save_db(user_id):
    file_name = str(user_id)
    db = shelve.open(file_name)
    db['now'] = dict_cost_type['now']
    db['products'] = dict_cost_type['products']
    db['eating_out'] = dict_cost_type['eating_out']
    db['transport'] = dict_cost_type['transport']
    db['purchases'] = dict_cost_type['purchases']
    db['home'] = dict_cost_type['home']
    db['entertainment'] = dict_cost_type['entertainment']
    db['services'] = dict_cost_type['services']
    db['all'] = dict_cost_type['all']


def open_db(user_id):
    file_name = str(user_id)
    db = shelve.open(file_name)
    dict_cost_type['now'] = db['now']
    dict_cost_type['products'] = db['products']
    dict_cost_type['eating_out'] = db['eating_out']
    dict_cost_type['transport'] = db['transport']
    dict_cost_type['purchases'] = db['purchases']
    dict_cost_type['home'] = db['home']
    dict_cost_type['entertainment'] = db['entertainment']
    dict_cost_type['services'] = db['services']
    dict_cost_type['all'] = db['all']


def arr_add(type_, user_id):
    cost = dict_cost_type['now']
    first_db(user_id)
    open_db(user_id)
    old_cost = dict_cost_type.get(type_)
    new_cost = old_cost + int(cost)
    old_all_cost = dict_cost_type.get('all')
    new_all_cost = old_all_cost + int(cost)
    dict_cost_type.update({type_: new_cost})
    # save_db(type_, user_id, new_cost)
    dict_cost_type.update({'all': new_all_cost})
    # dict_cost_type.update({'now': 0})
    save_db(user_id)

    # print(cost)
    # print(dict_cost_type)_
12

def types_cost(message):
    cost = int(message.text)
    # print(cost)

    # Создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_prod = types.InlineKeyboardButton(text='Продуты', callback_data='products')
    keyboard.add(key_prod)  # добавляем кнопку в клавиатуру
    key_eat = types.InlineKeyboardButton(text='Еда вне дома', callback_data='eating_out')
    keyboard.add(key_eat)
    key_transport = types.InlineKeyboardButton(text='Транспорт', callback_data='transport')
    keyboard.add(key_transport)
    key_purchases = types.InlineKeyboardButton(text='Покупки', callback_data='purchases')
    keyboard.add(key_purchases)
    key_home = types.InlineKeyboardButton(text='Дом. хоз-во', callback_data='home')
    keyboard.add(key_home)
    key_entertainment = types.InlineKeyboardButton(text='Развлечения', callback_data='entertainment')
    keyboard.add(key_entertainment)
    key_services = types.InlineKeyboardButton(text='Услуги', callback_data='services')
    keyboard.add(key_services)
    # key_exit = types.InlineKeyboardButton(text='Назад', callback_data='exit')
    # keyboard.add(key_exit)

    question = 'На что потрачено ' + str(cost) + ' руб' + ' ?'
    dict_cost_type['now'] = int(cost)
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "products":
        type_ = 'products'
        user_id = call.from_user.id
        # print(dict_cost_type['now'])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы потратили {0} руб на продукты'.format(dict_cost_type['now']))
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Cохранено!")
        arr_add(type_, user_id)
        # print(user_id, '-')
    elif call.data == "eating_out":
        type_ = 'eating_out'
        user_id = call.from_user.id
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы потратили {0} руб на еду вне дома'.format(dict_cost_type['now']))
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Cохранено!")
        arr_add(type_, user_id)
    elif call.data == "transport":
        type_ = 'transport'
        user_id = call.from_user.id
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы потратили {0} руб на транспорт'.format(dict_cost_type['now']))
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Cохранено!")
        arr_add(type_, user_id)
    elif call.data == "purchases":
        type_ = 'purchases'
        user_id = call.from_user.id
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы потратили {0} руб на покупки'.format(dict_cost_type['now']))
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Cохранено!")
        arr_add(type_, user_id)
    elif call.data == "home":
        type_ = 'home'
        user_id = call.from_user.id
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы потратили {0} руб на дом. хоз-во'.format(dict_cost_type['now']))
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Cохранено!")
        arr_add(type_, user_id)
    elif call.data == "entertainment":
        type_ = 'entertainment'
        user_id = call.from_user.id
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы потратили {0} руб на развлечения'.format(dict_cost_type['now']))
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Cохранено!")
        arr_add(type_, user_id)
    elif call.data == "services":
        type_ = 'services'
        user_id = call.from_user.id
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы потратили {0} руб на услуги'.format(dict_cost_type['now']))
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Cохранено!")
        arr_add(type_, user_id)
    # elif call.data == "exit":
    #     # call.message = '/start'
    #     # bot.register_next_step_handler(call.message, start_message)
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    #     # Уведомление в верхней части экрана
    #     bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Изменения сохранены")


bot.polling()
