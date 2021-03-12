import os
os.system('pip install pyautogui')
os.system('pip install keyboard')
os.system('pip install pillow')
os.system('pip install opencv-python')
import pyautogui as pg
import time as t
import keyboard as kb
import datetime as dt
import threading as td

def danger():
    try:
        if sum(pg.pixel(1235,1025)[:2])//2 >= 195 and not done():
            t.sleep(0.5)
            if sum(pg.pixel(1235,1025)[:2])//2 >= 195 and not done():
                print(pg.pixel(1235,1023))
                ext()
        if sum(pg.pixel(1370,1025)[:2])//2 >= 195 and not done():
            t.sleep(0.5)
            if sum(pg.pixel(1370,1025)[:2])//2 >= 195 and not done():
                print(pg.pixel(1369,1023))
                ext()
        if sum(pg.pixel(1270,1025)[:2])//2 >= 195 and not done():
            t.sleep(0.5)
            if sum(pg.pixel(1270,1025)[:2])//2 >= 195 and not done():
                print(pg.pixel(1270,1023))
                ext()
    except:
        return danger()
    else:
        t.sleep(1)

def bind_tea():
    kb.press('t')
    t.sleep(2)
    tea_location = pg.locateCenterOnScreen('images/tea.png', confidence = 0.75)
    if tea_location != None:
        pg.moveTo(tea_location)
        pg.dragTo(200, 850, 1)
    else:
        print('no tea found(')
    t.sleep(0.75)
    kb.release('t')

def is_ready():
    _ = pg.locateOnScreen('images/is_ready.png', confidence = 0.7)
    if _ != None:
        return True
    else:
        return False

def check_energy():
    #locate 280 955
    #on  167, 181, 51
    #off  90,  90, 88
    #print('check energy')
    if not is_eat:
        energy = False
    try:
        if pg.pixel(280,955)[1] <= 115:
            return True
    except:
        return check_energy()
    else:
        return False

def check_eat():
    #locate 280 990
    #on  167, 181, 51
    #off  90,  90, 88
    #print('check eat')
    try:
        if pg.pixel(280,990)[1] <= 115:
            return True
    except:
        return check_eat()
    else:
        return False

def frick(change):
    global fr
    t.sleep(0.15)
    prind('frick {:+}'.format(change))
    for i in range(abs(change)):
        pg.scroll(change//abs(change))
        fr += (change//abs(change))
        t.sleep(0.2)

def fish():
    #1625 980
    kb.send('r')
    t.sleep(0.25)
    if pg.locateOnScreen('images/fish.png', confidence = 0.85) != None:
        return True
    return False

def normalize_frick():
    global fr
    #1355 1050
    #1300 1050
    #1175 1050
    try:
        if pg.pixel(1350,1050)[1]>=155 and pg.pixel(566,1050)[1]>=155:
            #print('to a lot')
            frick(-1)

        elif sum(pg.pixel(1300,1050)[:2])/2<=155 and sum(pg.pixel(616,1050)[:2])/2<=155:
            #print('a few')
            if fr + 1<30:
                frick(1)
    except:
        normalize_frick()

def set_speed(value):
    kb.press('r')
    t.sleep(0.5)
    for i in range(50):
        pg.scroll(1)
        t.sleep(0.05)
    t.sleep(0.25)
    for i in range(50-value):
        pg.scroll(-1)
        t.sleep(0.05)
    t.sleep(0.25)
    kb.release('r')

def done():
    _ = pg.locateOnScreen('images/done.png', confidence = 0.65)
    if _ != None:
        return True
    return False

def eat():
    global is_eat
    if is_eat:
        pg.press('5')
    if pg.locateOnScreen('images/eatover.png', confidence = 0.85) != None:
        is_eat = False

def ext():
    log.close()
    print('turning off...')
    os.system('taskkill /F /IM rf4_x64.exe')
    exit()

def qit():
    log.close()
    print('turning off...')
    os.system('taskkill /F /IM python.exe')
    exit()

def zatsep():
    try:
        if pg.pixel(1305,1037)[0] >= 200 and pg.locateOnScreen('images/zatsep.png', confidence = 0.85) != None:
            print('zatsep')
            return True
    except:
        return zatsep()
    return False

def full():
    try:
        if sum(pg.pixel(1867,774))//3 >=225:
            return True
    except:
        return full()
    return False

def prind(value):
    global log
    print(value)
    log.write(value + '\n')

#STARTING

kb.add_hotkey('alt+l', qit)

if 'logs' not in os.listdir(path = '.'):
    os.system('mkdir logs')

log = open('logs/log_{}.txt'.format(t.ctime().replace(':', '-')), 'w')

timer = pg.prompt(text='Через сколько времени выключить бота и игру?', title='Таймер', default=None)
if timer != None and timer != '':
    start_time = t.time()
    need_time = start_time + float(timer) * 3600
else:
    timer = True

try:
    speed = int(pg.prompt(text='Какая скорость промотки?', title='Скорость', default=40))
except:
    pg.alert('Вы ввели не число, скорость установлена на 40')

try:
    mods = {"Твитчинг" : "twitching",
    "Джиговая ступенька" : 'djiging'}
    mode = mods[pg.confirm(text='Какой тип проводки?', title='Тип', buttons=['Твитчинг', 'Джиговая ступенька'])]
except:
    pg.alert('Ошибка, тип проводки установлен на твитчинг')
    mode = 'twitching'

for char in 'starting...':
    print(char, end = '', flush = True)
    t.sleep(0.1)

t.sleep(5)
fr = 25
bind_tea()
t.sleep(1.5)
set_speed(speed)
frick(-30)
frick(24)

checking = td.Thread(target = danger, name='checking_danger')
checking.start()

print("\nstarted succesfull")

is_eat = True
energy = True
fr = 25

time1 = t.time()

#MAINLOOP

while energy:

    try:
        if timer and t.time()>need_time:
            ext()
    except:
        pass

    if full():
        prind('full at time after start: H:{} M:{} S:{}'.format(int((t.time()-time1)//3600), int((t.time()-time1)//60), round((t.time()-time1)%60,1)))
        os.system('taskkill /F /IM rf4_x64.exe')
        exit()

    if is_ready():
        #vkid
        frick(25 - fr)
        t.sleep(0.5)
        prind('loop at time after start: H:{} M:{} S:{}'.format(int((t.time()-time1)//3600), int((t.time()-time1)//60), round((t.time()-time1)%60,1)))
        prind('vkid at time after start: H:{} M:{} S:{}'.format(int((t.time()-time1)//3600), int((t.time()-time1)//60), round((t.time()-time1)%60,1)))
        while check_eat():
            eat()
            t.sleep(0.25)
            kb.send('t')
            t.sleep(0.5)
        pg.mouseDown()
        t.sleep(3)
        pg.mouseUp()
        t.sleep(5)

    while not is_ready() and not fish() and not done():
        #twitching
        prind('{} at time after start: H:{} M:{} S:{}'.format(mode, int((t.time()-time1)//3600), int((t.time()-time1)//60), round((t.time()-time1)%60,1)))
        if mode == 'twitching':
            kb.press('shift')
            pg.mouseDown()
            t.sleep(0.5)
            pg.click(button = 'right')
            while zatsep():
                pg.mouseDown()
                pg.click(button='right')
                t.sleep(0.5)
            else:
                pg.mouseUp()
            pg.mouseUp()
            kb.release('shift')
            t.sleep(0.25)
        if mode == 'djiging':
            pg.mouseDown()
            t.sleep(2)
            while zatsep():
                pg.mouseDown()
                pg.click(button='right')
                t.sleep(0.5)
            else:
                pg.mouseUp()
            pg.mouseUp()
            t.sleep(2)

    else:
        if is_ready():
            continue

        if fish():
            #fishing
            prind('fishing at time after start: H:{} M:{} S:{}'.format(int((t.time()-time1)//3600), int((t.time()-time1)//60), round((t.time()-time1)%60,1)))
            pg.mouseDown()
            pg.mouseDown(button = 'right')
            while not done() and not is_ready():
                normalize_frick()
                while zatsep():
                    pg.mouseUp(button='right')
                    pg.click(button='right')
                    t.sleep(0.5)
                else:
                    pg.mouseDown(button='right')
                if check_energy():
                    eat()
            else:
                if not done():
                    continue
            pg.mouseUp(button = 'right')
            pg.mouseUp()
            while done():
                #accepting
                prind('accepting at time after start: H:{} M:{} S:{}'.format(int((t.time()-time1)//3600), int((t.time()-time1)//60), round((t.time()-time1)%60,1)))
                kb.send(' ')
                t.sleep(1)
else:
    ext()
