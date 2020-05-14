import csv
import subprocess
import time
import telebot
import os
from flask import Flask, request
import logging

bot = telebot.TeleBot('1141013801:AAEq32jIEQ0mjppuXm9t_XbldrXCDhVch3c')


class CheckBase:
    def __init__(self, csv1):
        self.csv1 = csv1
        self.base1 = {}
        self.base2 = {}
        self.message = ""

    def open(self):
        with open(self.csv1) as f:
            file = csv.DictReader(f, delimiter=",")
            self.base1 = {row["product_name"]: row["url"] for row in file}

    def check(self):
        for x in self.base1:
            if "ленд" in x or "Ленд" in x or "Сайт" in x or "сайт" in x or "верст" in x or "Верст" in x:
                if self.base2.get(x) == self.base1.get(x):
                    print("Найдено соответствие")
                else:
                    self.message += "{}\n{}\n\n".format(x, self.base1[x])

    def rewrite(self):
        self.base2 = self.base1
        f = open('fl-python.csv', 'r+')
        f.truncate()
        self.base1 = {}
        self.message = ""

bashCommand = "scrapy runspider fl/spiders/fl_title.py"

@bot.message_handler(commands=['start'])
def start_message(message):
    base = CheckBase("fl-python.csv")
    while True:
        subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        base.open()
        base.check()
        if base.message != "":
            bot.send_message(message.chat.id, base.message)
        base.rewrite()
        time.sleep(30)


# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://serene-peak-20980.herokuapp.com/bot") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
