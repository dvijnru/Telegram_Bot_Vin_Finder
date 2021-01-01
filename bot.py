import telebot
import config
from telebot import types
from selenium_parsing import selen_vin_check
from selenium_parsing import selen_nomer_check
import re
import time

bot = telebot.TeleBot(config.TOKEN)


# раздел для кнопок поиска
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Поиск по VIN')
item2 = types.KeyboardButton('Поиск по Госномеру')
markup.add(item1,item2)

# раздел для кнопок подтверждения начала нового поиска
again = types.ReplyKeyboardMarkup(resize_keyboard=True)
item3 = types.KeyboardButton('Да!')
again.add(item3)

# раздел приветственного сообщения пользователю после команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('starting_sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    text = 'Приветствую, Гость!\nБот предназначен для поиска информации по VIN или Госномеру автомобиля.\nДля дальнейшего использования, выберите нужную опцию поиска внизу.'
    bot.send_message(message.chat.id, text, reply_markup=markup)

# раздел для отправки ответных сообщений
@bot.message_handler(content_types=['text'])
def main_branch(message):
    if message.text == 'Поиск по VIN':
        bot.send_message(message.chat.id, 'Введите 17-ти значный VIN номер')
        bot.register_next_step_handler(message, enter_vin)

    if message.text == 'Поиск по Госномеру':
        bot.send_message(message.chat.id, 'Введите Госномер ТС в формате Х001ХХРРР, где Х - буквы русского алфавита нижнего или верхнего регистра, а РРР - двух- или трехзначный номер региона')
        bot.register_next_step_handler(message, enter_nomer)


def enter_vin(message):

    # запуск цепочки событий выбора, если пользователь нажимает кнопку другой опции.
    main_branch(message)

    if len(message.text) == 17:

        bot.send_message(message.chat.id, 'Обрабатываю запрос.\nРезультат будет отправлен через одну минуту.\nПожалуйста, подождите.')
        bot.send_message(message.chat.id, selen_vin_check(str(message.text).upper()))
        bot.send_message(message.chat.id, 'Для начала нового поиска, нажмите внизу соответствующую кнопку.', reply_markup=markup)
        return

    if message.text == 'Поиск по Госномеру':
        pass
    else:
        bot.send_message(message.chat.id, 'Указан некорректный идентификатор транспортного средства (VIN), попробуйте еще!')
        bot.register_next_step_handler(message, enter_vin)


def check_nomer(word):
    return bool(re.search('[АВЕКМНОРСТУХавекмнорстух]\d{3}[АВЕКМНОРСТУХавекмнорстух]{2}\d+', word))

def enter_nomer(message):

    # запуск цепочки событий выбора, если пользователь нажимает кнопку другой опции.
    main_branch(message)

    if check_nomer(str(message)) == True:
        bot.send_message(message.chat.id,'Зарегистрированные VIN:')
        bot.send_message(message.chat.id, selen_nomer_check(str(message.text).upper()))
        return

    if message.text == 'Поиск по VIN':
        pass

    else:
        bot.send_message(message.chat.id, 'Проверьте правильность символов и порядка их ввода. Допускаются только буквы АВЕКМНОРСТУХ как заглавные, так и прописные. Латинские символы недопустимы. ')
        bot.register_next_step_handler(message, enter_nomer)

# need to support working of bot
bot.polling(none_stop=True)

# есть баг при нажатии той же кнопки второй раз, процессы начинают дублироваться, потом количество увеличивается в два раза с каждым нажатием.
# как фиксить пока не знаю, помогает только перезапуск бота.
