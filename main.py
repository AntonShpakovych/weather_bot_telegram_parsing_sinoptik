
import requests
from bs4 import BeautifulSoup
import telebot
from setting import *
from datetime import datetime, time, timedelta

direction = {
    'Південний': '⬆️',
    'Північний': '⬇️',
    'Східний': '⬅️',
    'Західний': '➡️',
    'Південно-східний': '↖️',
    'Південно-західний': '↗️',
    'Північно-східний': '↙️',
    'Північно-західний': '↘️',
    'Штиль': '⏺',
}
global_param = {
    'Time': [],
    'Temp': [],
    'Press': [],
    'Humi': [],
    'Wind': [],
}
warning = {
    'Warn': 'Немає данних'
}


def show_data(d, w):
    copy_global_keys = []
    copy_global = []

    for i in range(len(d['Time'])):
        print(len(d['Time'][i]))
        if len(d['Time'][i]) == 6:
            d['Time'][i] = '0'+d['Time'][i]
    for key in d.keys():
        copy_global_keys.append(key)
    my_title = ''
    for i in range(len(copy_global_keys)):
        my_title += copy_global_keys[i]+'     '
    copy_global.append(my_title)
    for i in range(len(d[copy_global_keys[0]])):
        my_body = ''
        for j in range(len(copy_global_keys)):
            my_body += d[copy_global_keys[j]][i] + '      '
        copy_global.append(my_body)
    new_row = ''
    for i in range(len(copy_global)):
        new_row += copy_global[i]+'\n'
    new_row += '\n❗'+w['Warn'].upper()+'\n'
    for key in global_param.keys():
        global_param[key] = []
    warning['Warn'] = 'Немає данних'
    return new_row


bot = telebot.TeleBot(TOKEN)
# sinoptik


def data(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'lxml')
    tabs = soup.find('div', class_='tabs')
    main = tabs.find_all('div', class_='main')
    tbody = soup.find('tbody')
    all_tr = tbody.find_all('tr')
    # time
    tr_time = all_tr[0]
    td_time = tr_time.find_all('td')
    a_time = [i.text for i in td_time]
    for i in range(len(a_time)):
        global_param['Time'].append(a_time[i])
    # temp
    tr_temp = all_tr[2]
    td_temp = tr_temp.find_all('td')
    a_temp = [i.text for i in td_temp]
    for i in range(len(a_temp)):
        global_param['Temp'].append(a_temp[i])

    # tisk
    tr_tisk = all_tr[4]
    td_tisk = tr_tisk.find_all('td')
    a_tisk = [i.text for i in td_tisk]
    for i in range(len(a_tisk)):
        global_param['Press'].append(a_tisk[i])

    # humidity
    tr_humidity = all_tr[5]
    td_humidity = tr_humidity.find_all('td')
    a_humidity = [i.text for i in td_humidity]
    for i in range(len(a_humidity)):
        global_param['Humi'].append(a_humidity[i]+'%')

    # wind
    tr_wind = all_tr[6]
    td_wind = tr_wind.find_all('td')
    div_wind = tr_wind.find_all('div')
    arrow = [i.get('data-tooltip').split(',') for i in div_wind]
    a = []
    for i in range(len(arrow)):
        a.append(arrow[i][0])
    for i in range(len(a)):
        print(direction[a[i]])

    a_wind = [i.text for i in td_wind]
    for i in range(len(a_wind)):
        global_param['Wind'].append(a_wind[i]+direction[a[i]])

    # warning
    if soup.find('div', class_='oWarnings'):
        warning['Warn'] = soup.find('div', class_='oWarnings').text


@bot.message_handler(commands=['start'])  # може бути декілька параметрів
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)  # кнопки
    keyboard.row('/start', '/help', '/temperature')
    # відправляєм в чат ід хеллоу
    bot.send_message(
        message.chat.id, 'type button', reply_markup=keyboard)


@bot.message_handler(commands=['temperature'])  # внутрішні кнопкі
def button(message):
    url = 'https://ua.sinoptik.ua/погода-рівне'
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'lxml')
    tabs = soup.find('div', class_='tabs')
    main = tabs.find_all('div', class_='main')
    markup = telebot.types.InlineKeyboardMarkup()
    for i in range(len(main)):
        markup.add(telebot.types.InlineKeyboardButton(
            text=main[i].text, callback_data=i+1))
    bot.send_message(
        message.chat.id, text='Your info about temperature', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = ''
    bot.answer_callback_query(
        callback_query_id=call.id, text='You check some button!')

    if call.data == '1':
        url = 'https://ua.sinoptik.ua/погода-рівне'
        data(url)
        answer = show_data(global_param, warning)
    elif call.data == '2':
        for key in global_param.keys():
            global_param[key] = []
        url = f'https://ua.sinoptik.ua/погода-рівне/{datetime.today().date()+timedelta(days=1)}'
        data(url)
        answer = show_data(global_param, warning)
    elif call.data == '3':
        for key in global_param.keys():
            global_param[key] = []
        url = f'https://ua.sinoptik.ua/погода-рівне/{datetime.today().date()+timedelta(days=2)}'
        data(url)
        answer = show_data(global_param, warning)
    elif call.data == '4':
        for key in global_param.keys():
            global_param[key] = []
        url = f'https://ua.sinoptik.ua/погода-рівне/{datetime.today().date()+timedelta(days=3)}'
        data(url)
        answer = show_data(global_param, warning)
    elif call.data == '5':
        for key in global_param.keys():
            global_param[key] = []
        url = f'https://ua.sinoptik.ua/погода-рівне/{datetime.today().date()+timedelta(days=4)}'
        data(url)
        answer = show_data(global_param, warning)
    elif call.data == '6':
        for key in global_param.keys():
            global_param[key] = []
        url = f'https://ua.sinoptik.ua/погода-рівне/{datetime.today().date()+timedelta(days=5)}'
        data(url)
        answer = show_data(global_param, warning)
    elif call.data == '7':
        for key in global_param.keys():
            global_param[key] = []
        url = f'https://ua.sinoptik.ua/погода-рівне/{datetime.today().date()+timedelta(days=6)}'
        data(url)
        answer = show_data(global_param, warning)

    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() in ['hello', 'hi', 'ky']:
        bot.send_message(message.chat.id, 'Hello!')
    elif message.text.lower() == 'bye':
        bot.send_message(message.chat.id, 'Goodbye!')
    else:
        bot.send_message(message.chat.id, 'I dont understand')


bot.polling()
