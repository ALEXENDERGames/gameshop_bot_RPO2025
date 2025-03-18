import telebot
from user import *
from item import *
from telebot import types

bot = telebot.TeleBot("7791519532:AAGbG-AXgqCDn9NBDYD65FVdFeCddXIId8g")

admin_id = 475799956

gta = Item("GTA", "игра для народа",
           open("photos/gta.jpg", "rb"), 1000,
           "action", "6+")

witcher = Item("Witcher 3", "игра для борцов со злом",
           open("photos/whitcher.jpg", "rb"), 800,
           "action", "6+")

wukong = Item("Wukong", "игра для Влада",
           open("photos/wukong.jpg", "rb"), 2500,
           "action", "1+")

users = []
items = [gta, witcher, wukong]

@bot.message_handler(commands=["start", "help"])
def main(message):
    if check_user(message.from_user.id) == False:
        new_user = User(message.from_user.id,
                        message.from_user.first_name,
                        message.from_user.username)
        users.append(new_user)
        print(users)


    bot.send_message(message.chat.id, "Привет! 🎮 Добро пожаловать в нашего игрового бота! "
                                      "Здесь ты найдешь крутые игры по отличным ценам, эксклюзивные предложения "
                                      "и моментальную доставку. 🚀")

    menu_button = types.InlineKeyboardMarkup()
    shop = types.InlineKeyboardButton("посмотреть товары", callback_data="shop")
    admin = types.InlineKeyboardButton("обратиться к администратору", callback_data="admin")
    edit_profile = types.InlineKeyboardButton("редактировать профиль", callback_data="edit_profile")
    my_orders = types.InlineKeyboardButton("мои заказы", callback_data="my_orders")
    user_profile = types.InlineKeyboardButton("информация о профиле", callback_data="user_profile")

    for button in shop, admin, edit_profile, my_orders, user_profile:
        menu_button.row(button)

    bot.send_message(message.chat.id, "Выберите нужный пункт меню", reply_markup=menu_button)



@bot.callback_query_handler(func=lambda callback: True)
def main(callback):
    print(callback)
    id = callback.message.chat.id

    for item in items:
        if item.name == callback.data:
            item.show_info(id)

    match callback.data:
        case "shop":
            show_items(items, id)
        case "admin":
            bot.send_message(id, "обращение к админу")
            call_admin(callback.message)
        case "edit_profile":
            bot.send_message(id, "редактирование профиля")
        case "my_orders":
            bot.send_message(id, "Список ваших заказов")
        case "user_profile":
            for user in users:
                if user.id == callback.from_user.id:
                    user.show_info(user.id)
                    break
        #case _:
        #    bot.send_message(id, "данной команды пока что нет, просим прощения ☹")

def call_admin(message):
    message = bot.send_message(message.chat.id, "Введите вашу проблему:")
    bot.register_next_step_handler(message, send_admin)
def send_admin(message):
    bot.send_message(message.chat.id, "Данные отправленны администратору, он с вами свяжется")
    bot.send_message(admin_id, f"Запрос от @{message.from_user.username} \n"
                               f"Вопрос: {message.text}")
def check_user(id):
    is_user = False
    for user in users:
        if user.id == id:
            is_user = True
            break
    return is_user

def show_items(items, id):
    games = types.InlineKeyboardMarkup()
    for item in items:
        game = types.InlineKeyboardButton(item.name, callback_data=item.name)
        games.row(game)

    bot.send_message(id, "список игр: ", reply_markup=games)


bot.polling()
