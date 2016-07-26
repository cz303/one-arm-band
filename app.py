# -*- coding: utf-8 -*-
#Берегите глаза!
#тут говнокод
#v1.0
#не забудьте заменить token,apiKey и your_url_bot на свои значения :)
import telebot
from telebot import types
import os
from flask import Flask, request
import random as random_number
import requests
import json
import time
#
bot = telebot.TeleBot("TOKEN")
server = Flask(__name__)
#settings keyboards
keyboard = types.ReplyKeyboardMarkup()
keyboard.row(u"Играть",u"Правила")
keyboard.row(u"Баланс")
keyboard_hider = types.ReplyKeyboardHide()
kb_rate = types.ReplyKeyboardMarkup()
kb_rate.row(u"Ставлю 50",u"Ставлю 100")
kb_rate.row(u"Ставлю 1000")
kb_rate.row(u"Не хочу играть")
#
#
#commands handler
@bot.message_handler(commands=['start'])
def start(message):
     bot.send_message(message.chat.id, "Привет!", reply_markup=keyboard)
@bot.message_handler(commands=['help'])
def helpme(message):
     bot.send_message(message.chat.id,u"Жми играть и смотри, что тебе выпадет:\n\U0001f352\U0001f352\U0001f352 - x2\n\U0001f514\U0001f514\U0001f514 - x3\n\U0001f3c6\U0001f3c6\U0001f3c6 - x4\nЕсли в комбинации выпадет \U0001f3c6 , то гелиончики будут возмещены\nУдачи и больше выигрышей!" , reply_markup=keyboard)
@bot.message_handler(content_types=["text"])
#start game!
def game(message):
#balance receipt
    balance=requests.post("http://mighty-waters-23873.herokuapp.com/balance",data={"apiKey":"apiKey","username":message.from_user.username})
    money = balance.json()["balance"]
    if message.text == u"Играть":
         bot.send_message(message.chat.id,"Делайте ставку: ", reply_markup=kb_rate)
    elif message.text == u"Правила":
         bot.send_message(message.chat.id, u"Жми играть и смотри, что тебе выпадет:\n\U0001f352\U0001f352\U0001f352 - x2\n\U0001f514\U0001f514\U0001f514 - x3\n\U0001f3c6\U0001f3c6\U0001f3c6 - x4\nЕсли в комбинации выпадет \U0001f3c6 , то гелиончики будут возмещены\nУдачи и больше выигрышей!", reply_markup=keyboard)
    elif message.text == u"Ставлю 50":
         if money>50:
              r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":message.from_user.username,"receiver":"one_arm_bandit_bot","number":"50"})
              time.sleep(1)
              run(message,50)
         else:
              bot.send_message(message.chat.id,"Денег нет, но вы держитесь!",reply_markup=keyboard)
    elif message.text == u"Ставлю 100":
         if money>100:
              r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":message.from_user.username,"receiver":"one_arm_bandit_bot","number":"100"})
              time.sleep(1)
              run(message,100)
         else:
              bot.send_message(message.chat.id,"Денег нет, но вы держитесь!",reply_markup=keyboard)
    elif message.text == u"Ставлю 1000":
         if money>1000:
              r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":message.from_user.username,"receiver":"one_arm_bandit_bot","number":"1000"})
              time.sleep(1)
              run(message,1000)
         else:
              bot.send_message(message.chat.id,"Денег нет, но вы держитесь!",reply_markup=keyboard)
    elif message.text == u"Не хочу играть":
         bot.send_message(message.chat.id, "Возвращайся!", reply_markup=keyboard)
    elif message.text == u"Баланс":
         bot.send_message(message.chat.id,"Ваш баланс: " + str(money), reply_markup=keyboard)
def run(message,rate):
    balance=requests.post("http://mighty-waters-23873.herokuapp.com/balance",data={"apiKey":"apiKey","username":"one_arm_bandit_bot"})
    cash = balance.json()["balance"]
    a = u"\U0001f352"#cherry
    b = u"\U0001f514"#bell
    c = u"\U0001f3c6"#cup
    win1=[a,a,a]
    win2=[b,b,b]
    win3=[c,c,c]
    combination=[]
    smile=[a,b,c]
    while len(combination)<3:
        i = random_number.choice(smile)
        combination.append(i)
    bot.send_message(message.chat.id,combination[0]+combination[1]+combination[2], reply_markup=keyboard)
    if combination==win1:
        if cash>rate*2:
             bot.send_message(message.chat.id,"Вы выиграли %r гелиончиков!"%(rate*2), reply_markup=keyboard)
             r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":"one_arm_bandit_bot","receiver":message.from_user.username,"number":rate*2})
        else:
             bot.send_message(message.chat.id,"Упс...похоже в кассе бота недостаточно средств...Не волнуйтесь, ваши потраченные гелионы вернутся!\nЕсли не затруднит сообщите создателю бота об этом, мы во всем разберемся:)\n@enotcode", reply_markup=keyboard)
             r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":"one_arm_bandit_bot","receiver":message.from_user.username,"number":rate})
    elif combination==win2:
        if cash>rate*3:
             bot.send_message(message.chat.id,"Вы выиграли %r гелиончиков!"%(rate*3), reply_markup=keyboard)
             r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":"one_arm_bandit_bot","receiver":message.from_user.username,"number":rate*3})
        else:
             bot.send_message(message.chat.id,"Упс...похоже в кассе бота недостаточно средств...Не волнуйтесь, ваши потраченные гелионы вернутся!\nЕсли не затруднит сообщите создателю бота об этом, мы во всем разберемся:)\n@enotcode", reply_markup=keyboard)
             r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":"one_arm_bandit_bot","receiver":message.from_user.username,"number":rate})
    elif combination==win3:
        if cash>rate*4:
             bot.send_message(message.chat.id,"Вы выиграли %r гелиончиков!"%(rate*4), reply_markup=keyboard)
             r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":"one_arm_bandit_bot","receiver":message.from_user.username,"number":rate*4})
        else:
             bot.send_message(message.chat.id,"Упс...похоже в кассе бота недостаточно средств...Не волнуйтесь, ваши потраченные гелионы вернутся!\nЕсли не затруднит сообщите создателю бота об этом, мы во всем разберемся:)\n@enotcode", reply_markup=keyboard)
             r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":"one_arm_bandit_bot","receiver":message.from_user.username,"number":rate})
    elif c in combination!=0:
        bot.send_message(message.chat.id,"Вы ничего не выиграли, но гелиончики будут возмещены.", reply_markup=keyboard)
        r=requests.post("http://mighty-waters-23873.herokuapp.com/transfer", data={"apiKey":"apiKey","sender":"one_arm_bandit_bot","receiver":message.from_user.username,"number":rate})
    else:
        bot.send_message(message.chat.id,"Вы проиграли %r гелиончиков!"%(rate), reply_markup=keyboard)        
@server.route("/bot", methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="your_url_bot")
    return "OK", 200
server.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))
server = Flask(__name__)
