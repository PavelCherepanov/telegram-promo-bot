import telebot
import config
import random
from datetime import datetime, timedelta
import threading
import time

bot = telebot.TeleBot(config.TELEGRAM_API_TOKEN)
flag = False


def get_promo_code(num_chars):
    code_chars = config.CODE_CHARS
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start]
    return code


def generate_random_time():
    hour = str(random.randint(config.TIME_START_HOUR, config.TIME_END_HOUR))
    minutes = str(random.randint(
        config.TIME_START_MINUTES, config.TIME_END_MINUTES))
    if (minutes == "0"):
        minutes += str(random.randint(0, 9))
    if (
            minutes == "1" or minutes == "2" or minutes == "3" or minutes == "4" or minutes == "5" or minutes == "6" or minutes == "7" or minutes == "8" or minutes == "9"):
        minutes = "0" + minutes
    return str(str(hour) + ":" + str(minutes))


def check_time():
    while (True):
        random_time = generate_random_time()
        print(random_time)
        f = open("log.txt", "a")
        f.write(random_time + "\n")
        f.close()
        start = datetime.strptime(
            str((datetime.now() + timedelta(hours=4)).strftime("%H:%M")), "%H:%M")
        end = datetime.strptime(random_time, "%H:%M")
        time.sleep(int(60 * 60 * 24) - int(start.hour * 60 * 60 + start.minute * 60) + int(
            end.hour * 60 * 60 + end.minute * 60))
        global flag
        flag = True
        try:
            send_message_in_group()
        except:
            time.sleep(10)


@bot.message_handler(commands=["start", "help", "restart"])
@bot.message_handler(content_types=["text"])
def send_promo(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Получить промокод")
    markup.add(btn1)
    global flag
    if (flag == True):
        flag = False
        now_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        code = get_promo_code(6)
        f = open("log.txt", "a")
        f.write("[ " + now_time + " " + code + " ]" + "\n")
        f.close()
        bot.send_message(message.from_user.id,
                         config.SUCCESS_MESSAGE + code, reply_markup=markup)
        # get_answer(message)
        bot.send_message(config.ADMIN_ID, str(now_time) +
                         config.MESSAGE_FOR_ADMIN + code)
    else:
        bot.send_message(message.from_user.id,
                         config.FAIL_MESSAGE, reply_markup=markup)
        # get_answer(message)


# @bot.message_handler(content_types=["text"])
# def get_answer(message):
#     bot.send_message(message.chat.id, config.INFO_MESSAGE)

def send_message_in_group():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton(text=config.MESSAGE_CHANEL_TEXT_BUTTON, url=config.BOT_URL, callback_data=1))
    message = bot.send_message(
        config.GROUP_ID, config.MESSAGE_CHANEL_TEXT, reply_markup=markup)
    return message.id


if __name__ == "__main__":
    thr = threading.Thread(target=check_time)
    thr.start()
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            time.sleep(20)