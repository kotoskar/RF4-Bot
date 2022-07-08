from config import *
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
    print("installing packages...")
    os.system('pip install pyautogui')
    os.system('pip install keyboard')
    os.system('pip install pillow')
    os.system('pip install opencv-python')
    os.system('pip install pytelegrambotapi')
    import pyautogui as pg
    import time as t
    import keyboard as kb
    import datetime as dt
    import threading as td
    import telebot as tb
    from telebot import types

bot = tb.TeleBot('1872570952:AAF9_0j2UFFk6W3fGvK9wo2Bn8Tt__qeaiQ')


def send_screenshot():
    try:
        pg.screenshot('screen.png')
        with open('screen.png', 'rb') as img:
            bot.send_photo(id, img)
    except Exception as ex:
        send_screenshot()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        global check_fishes, first
        print('\ntelegram message from {}\n'.format(message.from_user.id))
        if message.from_user.id == id:
            print(msg := message.text.lower().split())
            match msg:
                case 'садок', *words:
                    check_fishes = True
                    bot.send_message(id, 'wait...')
                case 'скрин', *words:
                    send_screenshot()
                case 'выход', *words:
                    if not first:
                        close_game()
                case 'нажми', btn:
                    pg.press(btn)
                case 'зажми', btn:
                    pg.keyDown(btn)
                case 'отпусти', btn:
                    pg.keyUp(btn)
                case 'выполни', *words:
                    exec(''.join(words))
                case _:
                    bot.send_message(id, 'привет ^_^')
            first = False
    except Exception as ex:
        bot.send_message(id, str(ex))


def polling():
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as ex:
        polling()


def is_ready():
    try:
        return pg.locateOnScreen('images/is_ready.png', confidence=0.8) is not None
    except Exception as ex:
        return is_ready()


def need_energy():
    global energy
    if not is_eat:
        energy = False
    try:
        if pg.pixel(280, 955)[1] <= 115:
            return True
    except Exception as ex:
        return need_energy()
    else:
        return False


def change_friction(change):
    global friction
    t.sleep(0.035)
    print_and_log('friction {:+}'.format(change))
    for i in range(abs(change)):
        pg.scroll(change // abs(change))
        friction += (change // abs(change))
        t.sleep(0.035)


def is_fish():
    pg.press('r')
    t.sleep(0.25)
    try:
        return pg.locateOnScreen('images/fish.png', confidence=0.65) is not None
    except Exception as ex:
        return is_fish()


def normalize_friction():
    global last_friction_up
    try:
        while pg.pixel(1348, 1050)[0] >= 175 and pg.pixel(569, 1050)[0] >= 175:
            change_friction(-1)
        if sum(pg.pixel(1286, 1050)[:2]) / 2 <= 155 and sum(pg.pixel(630, 1050)[:2]) / 2 <= 155:
            if friction + 1 < 30 and t.time() - last_friction_up > 3:
                change_friction(1)
                last_friction_up = t.time()
    except Exception as ex:
        normalize_friction()


def set_friction(value):
    global friction
    friction = -10
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


def is_done():
    try:
        return pg.locateOnScreen('images/done.png', confidence=0.8) is not None
    except Exception as ex:
        return is_done()


def eat():
    global is_eat
    if is_eat:
        pg.press('5')
    try:
        if pg.locateOnScreen('images/eatover.png', confidence=0.85) is not None:
            is_eat = False
    except Exception as ex:
        eat()


def check_crash():
    try:
        return pg.locateOnScreen('images/crash.png', confidence=0.8) is not None
    except Exception as ex:
        return check_crash()


def is_near():
    try:
        return sum(pg.pixel(*default_size)) // 3 >= 155
    except Exception as ex:
        print(ex)
        return is_near()


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


def close_game():
    print_and_log('Выключение игры...')
    pg.mouseUp()
    pg.mouseUp(button='right')
    pg.keyUp('shift')
    os.system('taskkill /F /IM rf4_x64.exe')
    close_bot()


def close_bot():
    locker.acquire()
    print_and_log('Выключение бота...')
    if id is not None:
        bot.send_message(id, 'Выключение бота...')
        try:
            bot.send_document(id, open(log_path, 'rb'))
        except Exception as ex:
            bot.send_message(id, "Не удалось отправить лог:\n" + str(ex))
    log.close()
    os.system('taskkill /F /IM python.exe')
    exit()


def hot():
    return pg.pixel(1258, 1022)[0] >= 200 and sum(pg.pixel(1258, 1022)[1:]) <= 200


def lowline():
    return pg.pixel(1223, 1024)[0] >= 200 and sum(pg.pixel(1241, 1028)[1:]) <= 200


def zatsep():
    try:
        if (pix := pg.pixel(1305, 1037))[0] >= 200 and sum(pix[1:]) <= 200:
            print('zatsep')
            return True
    except Exception as ex:
        return zatsep()
    return False


def full():
    try:
        return pg.pixel(329, 239)[0] >= 120
    except Exception as ex:
        return full()


def print_and_log(value):
    global log
    print(
        f'{value} : [{round(t.time() - starts_time) // 3600}:{round(t.time() - starts_time) % 3600 // 60}:{round(t.time() - starts_time) % 60}]')
    log.write(
        f'{value} : [{round(t.time() - starts_time) // 3600}:{round(t.time() - starts_time) % 3600 // 60}:{round(t.time() - starts_time) % 60}]\n')


starts_time = t.time()
last_friction_up = starts_time

locker = td.Lock()

try:
    id = int(TELEGRAM_ID)
except ValueError:
    id = None

# HOTKEYS
kb.add_hotkey(EXIT_HOTKEY, close_bot)

# LOGS
path = os.path.dirname(os.path.abspath(__file__))
if 'logs' not in os.listdir(path=path):
    os.mkdir(path + '/logs')
log_path = 'logs/log_{}.txt'.format('-'.join(t.ctime().replace(':', '-').split()[-2:]))
log = open(log_path, 'w')

# EXIT TIMER
timer = pg.prompt(text='Через сколько часов выключить бота и игру?', title='Таймер', default=None)
if timer is not None and timer.isdigit():
    timer = True
    end_time = t.time() + float(timer) * 3600
else:
    timer = False

speed = int(pg.prompt(text='Какая скорость промотки?', title='Скорость', default=50))
def_fr = int(pg.prompt(text='Какой стандартный фрикцион?', title='Фрикцион', default=25))
mode = pg.confirm(text='Какой тип проводки?', title='Тип проводки',
                  buttons=['Твичинг', 'Джиговая ступенька', 'Рыскание', 'Пассивные Вэки', 'Равномерная'])

if id is None:
    pg.alert("Введите свой телеграм ID для дистанционного управления в файл 'config.py'", title='Телеграм ID')
    exit()

for char in 'starting...':
    print(char, end='', flush=True)
t.sleep(0.1)

is_eat = True
energy = True
check_fishes = False
first = True
friction = 25
is_zatsep = False
is_fish_now = False

td.Thread(target=polling, name='polling').start()

print_and_log("\nstarted successfully")

t.sleep(5)
set_speed(speed)

default_size = check_size()

while energy:
    print_and_log('LOOP')

    t.sleep(2)

    pg.press('shift')
    pg.mouseUp(button='right')
    pg.mouseUp()

    while is_done():
        print_and_log('ACCEPTING')
        if not FISH_FILTER or pg.locateOnScreen('images/trophy.png', confidence=0.8) is not None or pg.locateOnScreen(
                'images/nice.png', confidence=0.8) is not None or pg.locateOnScreen('images/rare.png',
                                                                                    confidence=0.8) is not None:
            if pg.locateOnScreen('images/trophy.png', confidence=0.8) is not None or pg.locateOnScreen(
                    'images/rare.png', confidence=0.8) is not None:
                send_screenshot()
            pg.press(' ')
        else:
            pg.press('backspace')
        t.sleep(0.75)

    if timer and t.time() > end_time:
        close_game()

    t.sleep(0.5)

    pg.press('c', interval=0.1)

    t.sleep(2.5)
    if pg.locateOnScreen('images/sadok.png') is not None:
        if full():
            print_and_log('FULL')
            close_game()
    else:
        t.sleep(3)
        if pg.locateOnScreen('images/sadok.png') is None:
            continue
        elif full():
            print_and_log('FULL')
            close_game()

    if check_fishes:
        send_screenshot()
        check_fishes = False

    pg.press('c', interval=0.1)

    t.sleep(1.5)

    if is_ready():
        set_friction(def_fr)
        t.sleep(0.25)
        print_and_log('THROWING')
        pg.mouseDown()
        t.sleep(3)
        pg.mouseUp()
        t.sleep(5)
    else:
        continue

    time1 = t.time()
    is_pressed = False
    while not (is_fish_now := is_fish()) and not is_ready() and not is_done():
        print_and_log(mode)

        while zatsep():
            pg.mouseDown()
            pg.click(button='right')
            t.sleep(0.5)

        match mode:
            case 'Рыскание':
                pg.keyDown('shift')
                pg.mouseDown()
                t.sleep(TIME_RISE)
                pg.mouseUp()
                pg.keyUp('shift')

            case 'Твичинг':
                t.sleep(TIME_BETWEEN_TWEETING)
                pg.keyDown('shift')
                pg.mouseDown()
                t.sleep(TIME_TWEETING)
                pg.click(button='right')
                pg.mouseUp()
                pg.keyUp('shift')

            case 'Джиговая ступенька':
                t.sleep(TIME_BETWEEN_TWEETING)
                pg.mouseDown()
                t.sleep(TIME_JUMPING)
                pg.mouseUp()

            case 'Пассивные Вэки':
                if t.time() - time1 >= TIME_BETWEEN_SLIDE:
                    pg.mouseDown()
                    t.sleep(TIME_SLIDE)
                    pg.mouseUp()
                    pg.press("enter")
                    time1 = t.time()

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
            while not is_done() and not is_ready():
                normalize_friction()
                if lowline() or check_crash():
                    t.sleep(1)
                    if lowline() or check_crash():
                        t.sleep(1)
                        if (low := lowline()) or (crash := check_crash()):
                            send_screenshot()
                            if low:
                                print_and_log('LOW!')
                            else:
                                print_and_log('CRASH!')
                        close_game()
                if hot():
                    print_and_log('HOT!')
                    pg.keyDown('enter')
                    while hot():
                        t.sleep(0.1)
                    pg.keyUp('enter')
                    pg.press('enter')
                if is_near():
                    pg.mouseDown(button='right')
                else:
                    pg.mouseUp(button='right')
                if need_energy():
                    eat()
                while zatsep():
                    pg.mouseUp(button='right')
                    pg.click(button='right')
                    t.sleep(0.5)
                t.sleep(0.05)

else:
    close_game()
