import telebot
from telebot import types
import time


import classData
import classPost
import cntrConsole

bot = telebot.TeleBot(open("token.txt").read())

Data = classData.DataBase()
Data.load()

cntrl = cntrConsole.Consl(Data,bot).run()


def addUser(mess):
    if not str(mess.chat.id) in Data.users.keys():
        Data.users[str(mess.chat.id)] = {"state":"","info": mess.from_user}

        print("Added new user",str(mess.chat.id))


def makeMurkup(id: int):

    """
    Meake Deafult Murkup with Button AddPost and Button for Admins
    :param id:
    :return:
    """

    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    predlosh = types.KeyboardButton("/Предложить запись")
    murkup.add(predlosh)
    if isAdmin(id):
        seepred = types.KeyboardButton("/(Админс команд)Просмотреть записи")
        murkup.add(seepred)

    return murkup


def SendPostFromProposed(post_id: str, user_id: str, to_admin: bool = False, reply_markup=None):
    post: classPost.Post = Data.proposed[post_id]

    if post.isOnlyText:
        bot.send_message(user_id, post.text, reply_markup=reply_markup)
    else:
        phts = []

        print(str(post.text))
        for i in post.media:
            phts += [types.InputMedia(i["type"], i["id"], caption=post.text)]

        bot.send_media_group(user_id, phts)

        if to_admin:
            bot.send_message(user_id,"⬆️⬆️⬆️Выложить пост выше?⬆️⬆️⬆️", reply_markup=reply_markup)

def SendPostAllUsers(post_id: str):
    for i in Data.users.keys():
        SendPostFromProposed(post_id, i)

# def SendPostFromPosts(post_id:str,user_id:str,to_admin:bool = False,reply_markup=None):
#     post: classPost.Post = Data.posts[post_id]
#
#     if post.isOnlyText:
#         bot.send_message(user_id, post.text, reply_markup=reply_markup)
#     else:
#         phts = []
#         for i in post.media:
#             phts += [types.InputMedia(i["type"], i["id"], caption=post.text)]
#
#         bot.send_media_group(user_id, phts)


def isAdmin(id:int):
    return str(id) in Data.admins.keys()


@bot.message_handler(commands=['start'])
def ComStart(message):
    addUser(message)
    murkup = makeMurkup(message.chat.id)
    bot.send_message(message.chat.id,"HI",reply_markup=murkup)


@bot.message_handler(content_types=["text", "photo", "voice", "audio", "document", "video"])
def re(message):

    addUser(message)

    print(Data.users[str(message.chat.id)])

    if message.text == "/Предложить запись":
        Data.users[str(message.chat.id)] = {"state":"NextMessageNews"}

        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        otmena = types.KeyboardButton("/Отмена")
        murkup.add(otmena)
        bot.send_message(message.chat.id, "Отправте вашу новость:", reply_markup=murkup)

    elif message.text == "/Отмена":
        Data.users[str(message.chat.id)] = {"state": ""}

        murkup = makeMurkup(message.chat.id)
        bot.send_message(message.chat.id, "Окей", reply_markup=murkup)

    elif message.text == "/(Админс команд)Просмотреть записи":
        if isAdmin(message.chat.id):



            # posts = list(Data.proposed.keys())

            postID = Data.GetOneProposed()
            if postID == None:
                murkup = makeMurkup(message.chat.id)
                bot.send_message(chat_id=str(message.chat.id), text="Посты кончились", reply_markup=murkup)
                return

            bot.send_message(message.chat.id, "Очередной высер:", reply_markup=types.ReplyKeyboardRemove())

            murkup = types.InlineKeyboardMarkup()

            b_yes = types.InlineKeyboardButton(text="Запостить✅", callback_data=f"POST {postID}")
            # murkup.add(b_yes)

            b_potom = types.InlineKeyboardButton(text="Отложить⏳", callback_data=f"NEXT {postID}")
            # murkup.add(b_potom)

            b_No = types.InlineKeyboardButton(text="Удалить❌", callback_data=f"DEL {postID}")

            murkup.add(b_yes, b_potom, b_No)

            SendPostFromProposed(postID, str(message.chat.id), reply_markup=murkup,to_admin=True)

            murkup = makeMurkup(message.chat.id)
            bot.send_message(chat_id=str(message.chat.id), text="решай)", reply_markup=murkup)

    elif Data.users[str(message.chat.id)]["state"] == "NextMessageNews":
        Data.users[str(message.chat.id)] = {"state": ""}
        Data.addProposed(message)

        murkup = makeMurkup(message.chat.id)
        bot.send_message(message.chat.id, "Принято приятно", reply_markup=murkup)

    elif str(message.media_group_id) in Data.proposed.keys():
        Data.addPost(message)

    else:
        murkup = makeMurkup(message.chat.id)
        bot.send_message(message.chat.id, "это что", reply_markup=murkup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    if call.message:

        if call.data == "-":
            return

        print("NOT inline", call.data)
        murkup = types.InlineKeyboardMarkup()
        btext = "-"
        comm = call.data.split()[0]

        if comm == "POST":
            btext = "✅"
        elif comm == "NEXT":
            btext = "⏳"
        elif comm == "DEL":
            btext = "❌"

        par = call.data.split()[1]

        if par in Data.proposed.keys():

            if comm == "POST":
                SendPostAllUsers(par)
                Data.EditProposed(par, "acceptedAdmin", call.message.from_user.username)
                Data.MoveProposedInPost(par)

            elif comm == "NEXT":
                Data.EditProposed(par, "priority", Data.proposed[par].priority + 1)

            elif comm == "DEL":
                Data.EditProposed(par, "priority", Data.proposed[par].priority + 10000)
                Data.EditProposed(par, "IsDel", True)

        else:
            btext = "этого поста больше нет"

        EmtyButton = types.InlineKeyboardButton(text=btext, callback_data="-")  # ❌ ✅ ⏳
        murkup.add(EmtyButton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=murkup, text=call.message.text)



bot.polling(none_stop=True)