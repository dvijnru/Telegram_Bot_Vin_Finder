import telebot
import config
from telebot import types
from selenium_parsing import selen_vin_check
import time

bot = telebot.TeleBot(config.TOKEN)


# раздел для кнопок поиска
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Поиск по VIN')
item2 = types.KeyboardButton('Поиск по Госномеру')
markup.add(item1,item2)


# раздел приветственного сообщения пользователю после команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('starting_sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    text = 'Приветствую, Гость!\nБот предназначен для поиска информации по VIN или Госномеру автомобиля.\nДля дальнейшего использования, выберите нужную опцию поиска внизу.'
    #text2 = str(bot.getMe(first_name))
    bot.send_message(message.chat.id, text, reply_markup=markup)

# раздел для отправки ответных сообщений
@bot.message_handler(content_types=['text'])
def vin_branch(message):
    if message.text == 'Поиск по VIN':
        bot.send_message(message.chat.id, 'Введите 17-ти значный VIN номер')
        bot.register_next_step_handler(message, enter_vin)

def enter_vin(message):
    if len(message.text) == 17:
        # нужна проверка RE чтобы были только буквы и цифры
        bot.send_message(message.chat.id, 'Обрабатываю запрос.\nРезультат будет отправлен через одну минуту.\nПожалуйста, подождите.')
        bot.send_message(message.chat.id, selen_vin_check(str(message.text).upper()))

        # отправляем ответное сообщение с информацией
    else:
        bot.send_message(message.chat.id, 'Указан некорректный идентификатор транспортного средства (VIN), попробуйте еще!')
        bot.register_next_step_handler(message, vin_branch)


###
bot.polling(none_stop=True)

'''
TEST_VIN = 'VF32CKFXF40551972'
print(selen_vin_check(TEST_VIN))
'''