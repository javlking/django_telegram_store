import telebot
from telebot import types
from . import models
bot = telebot.TeleBot('5105426169:AAHwY7PxbqB1g78HYcyG43-OBZE0s5Nes9E')

# Создаем словарь для временного хранения продуктов при добавлении
product = {'name': None,
           'photo_id': None,
           'price': None}
user_cart = {'user_id': {
    'product_name': None,
    'product_count': None}}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    # Получаем список состящий из названиев
    o = models.ProductName.objects.all()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button = []
    for butto in o:
        button.append(*butto.name)

    keyboard.add(*button)
    keyboard.add(types.KeyboardButton('Корзина'))

    bot.send_message(user_id, 'Добро пожаловать в наш бот', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text(message):
    # Получаем все товары из базы
    user_id = message.from_user.id
    o = models.ProductName.objects.all()
    user_cart[user_id] = {}

    print(user_cart)
    items = []
    for item in o:
        items.append(item.name)

    # Проверяем есть ли у нас в базе товар с именем который отправит пользователь
    if message.text in items:
        user_cart[user_id]['product_name'] = message.text  #

        product = data.User().get_info(message.text)

        # Параметр row_width щтвечает за количество кнопок в одной строке
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

        # Создаем кнопки для выбора количества
        i = [str(o) for o in range(1, 10)]
        keyboard.add(*i)

        # Если то что выбрал пользователь есть у нас в базе то отправляем ему фото, имя и цену товара
        # Метод .send_photo(кому, какое фото, текст к нему, кнопки(если есть)) отвечает за отправку фото и текст к нему(если имеется)
        bot.send_photo(message.from_user.id, f'{product[0][1]}', f'{product[0][0]}\n\nЦена: {product[0][-1]}',
                       reply_markup=keyboard)

        bot.register_next_step_handler(message, get_quantity)

    # если пользователь нажмет на кнопку корзина мв из базы достаем его товары
    elif message.text == 'Корзина':
        user_id = message.from_user.id

        y = 'Ваша корзина:'
        # Здесь .full_cart(user_id) этот метод как аргумент будет братьайди юзера чтобы вывести конкретно его товары
        t = data.User().full_cart(user_id)
        cart_items = "\n\n{name} \n{count} шт"

        for i in t:
            korzina = cart_items.format(name=i[0],
                                        count=i[1])
            y += korzina
        # print(korzina)

        bot.send_message(user_id, y)


def get_quantity(message):
    user_id = message.from_user.id
    count = message.text
    user_cart[user_id]['product_count'] = int(count)  #

    data.User().get_cart(user_id, user_cart[user_id]['product_name'], user_cart[user_id]['product_count'])
    bot.send_message(user_id, 'Продукт успешно добавлен')

    # После добавления продукта в корзину нас перекидывет на этап выбора продуктов
    start(message)


bot.polling(non_stop=True)