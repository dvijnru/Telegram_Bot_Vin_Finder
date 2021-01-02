import telebot
import config
from telebot import types
from selenium_parsing import selen_vin_check
from selenium_parsing import selen_nomer_check
from selenium_parsing import selen_deep_VIN_check
import re

bot = telebot.TeleBot(config.TOKEN)


# раздел для кнопок поиска
main_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Поиск по VIN')
item2 = types.KeyboardButton('Поиск по Госномеру')
main_buttons.add(item1, item2)

# раздел для кнопок подтверждения начала нового поиска
deep_check = types.ReplyKeyboardMarkup(resize_keyboard=True)
item3 = types.KeyboardButton('Да!')
item4 = types.KeyboardButton('Нет, спасибо.')
deep_check.add(item3, item4)

# раздел приветственного сообщения пользователю после команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('starting_sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    text = 'Приветствую, Гость!\nБот предназначен для поиска информации по VIN или Госномеру автомобиля.\nДля дальнейшего использования, выберите нужную опцию поиска внизу.'
    bot.send_message(message.chat.id, text, reply_markup=main_buttons)

# ветка для ловли сообщений из главного меню
@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Поиск по VIN':
        bot.send_message(message.chat.id, 'Введите 17-ти значный VIN номер')
        bot.register_next_step_handler(message, enter_vin)

    if message.text == 'Поиск по Госномеру':
        bot.send_message(message.chat.id, 'Введите Госномер ТС в формате Х001ХХРРР, где Х - буквы русского алфавита нижнего или верхнего регистра, а РРР - двух- или трехзначный номер региона')
        bot.register_next_step_handler(message, enter_nomer)

# проверка вин на корректность ввода
def check_VIN_for_correct(word):
    return bool(re.search('\w{17}', word))

# запуск ветки проверки по вин
def enter_vin(message):

    # запуск цепочки событий выбора, если пользователь нажимает кнопку другой опции.
    main_menu(message)

    if check_VIN_for_correct(str(message.text)) == True:

        bot.send_message(message.chat.id, 'Обрабатываю запрос.\nРезультат будет отправлен через одну минуту.\nПожалуйста, подождите.')
        bot.send_message(message.chat.id, selen_vin_check(str(message.text).upper()))
        bot.send_message(message.chat.id, 'Для начала нового поиска нажмите внизу соответствующую кнопку.')
        # bot.send_message(message.chat.id, 'Выполнить проверку VIN на наличие ДТП, федерального розыска и ограничений?', reply_markup=deep_check)
        return

    if message.text == 'Поиск по Госномеру':
        return

    if message.text == 'Поиск по VIN':
        return

    else:
        bot.send_message(message.chat.id, 'Указан некорректный идентификатор транспортного средства (VIN), попробуйте еще!')
        bot.register_next_step_handler(message, enter_vin)


# проверки номера на корректность
def check_nomer(word):
    return bool(re.search('[АВЕКМНОРСТУХавекмнорстух]\d{3}[АВЕКМНОРСТУХавекмнорстух]{2}\d+', word))

# запуск ветки проверки по госномеру
def enter_nomer(message):

    # запуск цепочки событий выбора, если пользователь нажимает кнопку другой опции.
    main_menu(message)

    if message.text == 'Поиск по Госномеру':
        return

    if message.text == 'Поиск по VIN':
        return

    if check_nomer(str(message)) == True:
        bot.send_message(message.chat.id, selen_nomer_check(str(message.text).upper()))
        bot.send_message(message.chat.id, 'Для начала нового поиска нажмите внизу соответствующую клавишу.')
        return

    else:
        bot.send_message(message.chat.id, 'Проверьте правильность символов и порядка их ввода. Допускаются только буквы АВЕКМНОРСТУХ как заглавные, так и прописные. Латинские символы недопустимы. ')
        bot.register_next_step_handler(message, enter_nomer)


# need to support working of bot
bot.polling(none_stop=True)


# черновик для следующей фичи - дальнейшей проверки по вин после успешного завершения.
'''
if message.text == 'Да!':
    bot.send_message(message.chat.id, selen_deep_VIN_check())
'''