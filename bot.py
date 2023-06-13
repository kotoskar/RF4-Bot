# IMPORTS --------------------------------------------------------------------------------------------------------------
import random

from cfg import *
import os

try:
    import pyautogui as pg
    import time as t
    import keyboard as kb
    import datetime as dt
    import threading as td
    import telebot as tb
    from telebot import types
except ImportError:
    from setup import setup

    setup()

    import pyautogui as pg
    import time as t
    import keyboard as kb
    import datetime as dt
    import threading as td
    import telebot as tb
    from telebot import types

# GLOBALS --------------------------------------------------------------------------------------------------------------

# BOT1 = '1872570952:AAF9_0j2UFFk6W3fGvK9wo2Bn8Tt__qeaiQ'
# https://t.me/RF4FishingBot
# BOT2 = '5397438580:AAFgCAv34MSNw7zIZDYFAUvxHccm09LhXF4'
# https://t.me/RF4Fishing_Bot
BOT_API_KEY = '5397438580:AAFgCAv34MSNw7zIZDYFAUvxHccm09LhXF4'

bot = tb.TeleBot(BOT_API_KEY)

locker = td.Lock()

starts_time = t.time()
last_friction_change = starts_time
alive = True
check_fishes = False
first_message = True
friction = 25
is_fish_now = False
last_rise = starts_time

try:
    tg_id = int(TELEGRAM_ID)
except ValueError:
    pg.alert("Введите свой телеграм ID для дистанционного управления в файл 'settings.py'", title='Телеграм ID')
    exit()

timer = pg.prompt(text='Через сколько часов выключить бота и игру?', title='Таймер', default=None)
if timer is not None and timer.isdigit():
    timer = True
    end_time = t.time() + float(timer) * 3600
else:
    timer = False

speed = int(pg.prompt(text='Какая скорость промотки?', title='Скорость', default=50))
default_friction = int(pg.prompt(text='Какой стандартный фрикцион?', title='Фрикцион', default=25))
mode = pg.confirm(text='Какой тип проводки?', title='Тип проводки',
                  buttons=['Твичинг', 'Джиговая ступенька', 'Рыскание', 'Равномерная'])


# CHECKERS -------------------------------------------------------------------------------------------------------------
def done():
    try:
        return pg.locateOnScreen('images/done.png', confidence=0.8) is not None
    except Exception as ex:
        return done()


def ready():
    try:
        return pg.locateOnScreen('images/is_ready.png', confidence=0.8) is not None
    except Exception as ex:
        return ready()


def need_energy():
    try:
        if pg.pixel(280, 955)[1] <= 115:
            return True
    except Exception as ex:
        return need_energy()
    else:
        return False


def fish():
    pg.press('r')
    t.sleep(0.25)
    try:
        return pg.locateOnScreen('images/fish.png', confidence=0.65) is not None
    except Exception as ex:
        return fish()


def full_friction():
    try:
        return sum(pg.pixel(955, 940)) / 3 >= 255
    except Exception as ex:
        return full_friction()


def crash():
    try:
        return pg.locateOnScreen('images/crash.png', confidence=0.8) is not None
    except Exception as ex:
        return crash()


def near():
    try:
        return sum(pg.pixel(*default_size)) // 3 >= 155
    except Exception as ex:
        print(ex)
        return near()


def check_size():
    sizes = [(1237, 1010), (1240, 1010), (1243, 1011), (1246, 1013), (1248, 1016), (1250, 1019), (1250, 1022),
             (1250, 1025), (1249, 1028), (1248, 1031), (1246, 1033), (1244, 1035), (1241, 1036), (1238, 1036),
             (1235, 1036), (1232, 1036), (1229, 1035), (1227, 1033), (1225, 1030), (1224, 1027), (1223, 1024),
             (1223, 1021), (1224, 1018), (1225, 1015), (1227, 1013), (1230, 1011), (1233, 1010), (1236, 1010)]
    try:
        for i in range(len(sizes)):
            if sum(pg.pixel(*sizes[i])) // 3 < 155:
                return sizes[i - 2]
    except Exception as ex:
        print(ex)
        return check_size()
    else:
        return sizes[-2]


def overheating():
    return pg.pixel(1258, 1022)[0] >= 200 >= sum(pg.pixel(1258, 1022)[1:])


def low_line():
    return pg.pixel(1223, 1024)[0] >= 200 >= sum(pg.pixel(1241, 1028)[1:])


def hooked():
    try:
        if (pix := pg.pixel(1305, 1037))[0] >= 200 >= sum(pix[1:]):
            print('zatsep')
            return True
    except Exception as ex:
        return hooked()
    return False


def full():
    try:
        return pg.pixel(329, 239)[0] >= 120
    except Exception as ex:
        return full()


# FUNCTIONS ------------------------------------------------------------------------------------------------------------
def send_screenshot():
    try:
        pg.screenshot('screen.png')
        with open('screen.png', 'rb') as img:
            bot.send_photo(tg_id, img)
    except Exception as ex:
        send_screenshot()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        global check_fishes, first_message
        print('\ntelegram message from {}\n'.format(message.from_user.tg_id))
        if message.from_user.tg_id == tg_id:
            print(msg := message.text.lower().split())
            match msg:
                case 'садок', *words:
                    check_fishes = True
                    bot.send_message(tg_id, 'wait...')
                case 'скрин', *words:
                    send_screenshot()
                case 'выход', *words:
                    if not first_message:
                        close_game()
                case 'нажми', btn:
                    pg.press(btn)
                case 'зажми', btn:
                    pg.keyDown(btn)
                case 'отпусти', btn:
                    pg.keyUp(btn)
                case 'выполни', *words:
                    exec(' '.join(words))
                case 'help', *words:
                    bot.send_message(tg_id, 'садок\nскрин\nвыход\nнажми\nзажми\nотпусти\nвыполни')
                case _:
                    bot.send_message(tg_id, 'привет ^_^')
            first_message = False
    except Exception as ex:
        bot.send_message(tg_id, str(ex))


def polling():
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as ex:
        t.sleep(1.5)
        polling()


def change_friction(change):
    global friction
    t.sleep(0.035)
    print_and_log('friction {:+}'.format(change))
    for i in range(abs(change)):
        pg.scroll(change // abs(change))
        friction += (change // abs(change))
        t.sleep(0.035)


def normalize_friction():
    global last_friction_change, friction
    try:
        while pg.pixel(1320, 1050)[0] >= 175 and pg.pixel(597, 1050)[0] >= 175:
            change_friction(-1)
        if sum(pg.pixel(1266, 1050)[:2]) / 2 <= 155 and sum(pg.pixel(650, 1050)[:2]) / 2 <= 155:
            if friction + 1 < 30 and t.time() - last_friction_change > 4:
                change_friction(1)
                if full_friction():
                    friction = 30
                    change_friction(-1)
        last_friction_change = t.time()
    except Exception as ex:
        normalize_friction()


def set_friction(value):
    global friction
    friction = 0
    change_friction(30)
    change_friction(value - 30)
    friction = value


def set_speed(value):
    pg.keyDown('r')
    t.sleep(0.25)
    for i in range(50):
        pg.scroll(1)
        t.sleep(0.035)
    t.sleep(0.25)
    for i in range(50 - value):
        pg.scroll(-1)
        t.sleep(0.035)
    t.sleep(0.25)
    pg.keyUp('r')


def eat():
    global alive
    pg.press('5')
    try:
        if pg.locateOnScreen('images/eatover.png', confidence=0.85) is not None:
            alive = False
    except Exception as ex:
        eat()


def close_game():
    os.system('taskkill /F /IM rf4_x64.exe')
    print_and_log('Выключение игры...')
    pg.mouseUp()
    pg.mouseUp(button='right')
    pg.keyUp('shift')
    close_bot()


def close_bot():
    locker.acquire()
    print_and_log('Выключение бота...')
    log.close()
    if tg_id is not None:
        bot.send_message(tg_id, 'Выключение бота...')
        try:
            bot.send_document(tg_id, open(log_path, 'rb'))
        except Exception as ex:
            bot.send_message(tg_id, "Не удалось отправить лог:\n" + str(ex))
    os.system('taskkill /F /IM python.exe')
    exit()


def print_and_log(value):
    global log
    time = t.time() - starts_time
    print(
        f'{value} : [{round(time) // 3600}:{round(time) % 3600 // 60}:{round(time) % 60}]')
    log.write(
        f'{value} : [{round(time) // 3600}:{round(time) % 3600 // 60}:{round(time) % 60}]\n')


def accept_fish():
    while done():
        print_and_log('ACCEPTING')
        marked = pg.locateOnScreen('images/marked.png', confidence=0.8) is not None
        trophy = pg.locateOnScreen('images/trophy.png', confidence=0.8) is not None
        rare_trophy = pg.locateOnScreen('images/rare_trophy.png', confidence=0.8) is not None
        if trophy or rare_trophy:
            send_screenshot()
        if not FISH_FILTER or any([marked, trophy, rare_trophy]):
            pg.press(' ')
        else:
            pg.press('backspace')
        t.sleep(0.75)


def check_sadok():
    global check_fishes

    t.sleep(0.5)

    pg.press('c', interval=0.1)

    t.sleep(0.75)
    if pg.locateOnScreen('images/sadok.png') is not None:
        if full():
            print_and_log('FULL')
            close_game()
    else:
        t.sleep(3)
        if pg.locateOnScreen('images/sadok.png') is None:
            check_sadok()
        elif full():
            print_and_log('FULL')
            close_game()

    if check_fishes:
        send_screenshot()
        check_fishes = False

    pg.press('c', interval=0.1)

    t.sleep(0.75)


def cast():
    t.sleep(0.25)
    print_and_log('THROWING')
    pg.keyDown('shift')
    pg.mouseDown()
    t.sleep(1)
    pg.mouseUp()
    pg.keyUp('shift')
    t.sleep(random.uniform(3, 5))


def rise():
    pg.keyDown('shift')
    pg.mouseDown()
    t.sleep(TIME_RISE)
    pg.mouseUp()
    pg.keyUp('shift')


def twitch():
    pg.keyDown('shift')
    pg.mouseDown()
    t.sleep(TIME_TWEETING)
    pg.click(button='right')
    pg.mouseUp()
    pg.keyUp('shift')


def jigging():
    pg.mouseDown()
    t.sleep(TIME_JUMPING)
    pg.mouseUp()


def fishing(func, time_between=0):
    global last_rise
    if t.time() - last_rise > time_between:
        func()
        last_rise = t.time()


# HOTKEYS --------------------------------------------------------------------------------------------------------------
kb.add_hotkey(EXIT_HOTKEY, close_bot)

# LOGS -----------------------------------------------------------------------------------------------------------------
path = os.path.dirname(os.path.abspath(__file__))
print('cd ' + path)
print('python bot.py')
if 'logs' not in os.listdir(path=path):
    os.mkdir('/logs')
log_path = path + '/logs/log_{}.txt'.format('-'.join(t.ctime().replace(':', '-').split()[-2:]))
log = open(log_path, 'w')

print_and_log("\nstarted successfully")

td.Thread(target=polling, name='polling').start()

# START ----------------------------------------------------------------------------------------------------------------
t.sleep(5)
set_speed(speed)

default_size = check_size()

while alive:
    print_and_log('LOOP')

    t.sleep(0.5)

    pg.press('shift')
    pg.mouseUp(button='right')
    pg.mouseUp()

    if crash():
        print_and_log('CRASHED')
        close_game()

    if done():
        accept_fish()

    if timer and t.time() > end_time:
        close_game()

    check_sadok()

    if ready():
        change_friction(default_friction - friction)
        cast()
    else:
        continue

    time1 = t.time()
    is_pressed = False
    while not (is_fish_now := fish()) and not ready() and not done():
        print_and_log(mode)

        while hooked():
            pg.mouseDown()
            pg.click(button='right')
            t.sleep(0.5)

        match mode:
            case 'Рыскание':
                fishing(rise)

            case 'Твичинг':
                fishing(twitch, TIME_BETWEEN_TWEETING)

            case 'Джиговая ступенька':
                fishing(jigging, TIME_BETWEEN_JUMPING)

            case 'Равномерная':
                if not is_pressed:
                    pg.mouseDown()
                    is_pressed = True

    else:
        pg.mouseUp()
        pg.mouseUp(button='right')
        pg.keyUp('shift')
        if is_fish_now:
            print_and_log("FISH!")
            pg.mouseDown()
            pg.keyDown('shift')
            t.sleep(0.05)
            while not done() and not ready() and not crash():
                normalize_friction()
                if low_line():
                    t.sleep(0.75)
                    if low_line():
                        send_screenshot()
                        print_and_log('LOW LINE')
                        close_game()

                if overheating():
                    print_and_log('OVERHEAT!')
                    pg.mouseUp()
                    t.sleep(0.2)
                    pg.keyDown('enter')
                    while overheating() and not low_line():
                        t.sleep(0.1)
                    if low_line():
                        send_screenshot()
                        print_and_log('LOW LINE')
                        close_game()
                    pg.keyUp('enter')
                    pg.mouseDown()

                if near():
                    pg.mouseDown(button='right')
                else:
                    pg.mouseUp(button='right')

                if need_energy():
                    eat()

                while hooked():
                    pg.mouseUp(button='right')
                    pg.click(button='right')
                    t.sleep(0.5)

                t.sleep(0.05)

else:
    close_game()
