import telebot
import config
import re
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

###
# раздел для кнопки старт /start
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Поиск по VIN')
item2 = types.KeyboardButton('Поиск по Госномеру')
markup.add(item1,item2)

###

###
#раздел приветственного сообщения пользователю после команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('starting_sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    text = 'Приветствую, %username%!\nДля дальнейшего использования, выберите нужную опцию поиска внизу'
    #text2 = str(bot.getMe(first_name))
    bot.send_message(message.chat.id, text, reply_markup=markup)
###

def FindByVIN(VIN):
    # здесь код запроса к базе ГИБДД
    return(VIN)

###
# раздел для отправки ответных сообщений
@bot.message_handler(content_types=['text'])
def lalala0(message):
    if message.text == 'Поиск по VIN':
        bot.send_message(message.chat.id, 'Введите 14-ти значный VIN номер')

        #нужно заново ловить новое сообщение и распознать его как message
        @bot.message_handler(content_types=['text'])
        def lalala1(message1):
            if len(message1.text) == 14 :
                bot.send_message(message1.chat.id, 'Отлично, веду поиск по VIN')
                FindByVIN(message1.text)
            else:
                bot.send_message(message1.chat.id, 'Неправильный вин, попробуйте еще!')

    if message.text == 'Поиск по Госномеру':
        bot.send_message(message.chat.id, 'Отлично, веду поиск по Госномеру')
        #здесь код запроса к ресурсу VIN01.ru для получения вина, потом подставляем в функцию поиска по вин FindByVIN

###

bot.polling(none_stop=True)
