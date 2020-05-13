import csv
import subprocess
import time
import telebot

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


if __name__ == "__main__":
    base = CheckBase("fl-python.csv")
    bashCommand = "scrapy runspider fl/spiders/fl_title.py"

    @bot.message_handler(commands=['start'])
    def start_message(message):
        i = 0
        while i < 60000:
            subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            base.open()
            base.check()
            if base.message != "":
                bot.send_message(message.chat.id, base.message)
            base.rewrite()
            time.sleep(60)
            i += 1


    bot.polling()
