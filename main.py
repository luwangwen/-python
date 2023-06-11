import json
import pyautogui as ag
import keyboard as kb
import sys
import time

title = '按键精灵'

points: list = [ag.position()]
recorder: list = []
todo: list = []

t: float
sleep_flag: bool = True


def main():
    global todo, title

    mode = ag.confirm(text='mode', title=title, buttons=['recording', 'playback'])
    if mode == 'recording':
        recording()
    else:
        choose()


def choose():
    global title, todo
    try:
        with open('script.json') as f:
            text: dict = json.load(f)
            todo = text['data']
            pos: list = text['pos']
    except FileNotFoundError:
        print('Please recording first')
        main()

    mode = ag.confirm(text='mode', title=title, buttons=['absolute', 'relative'])
    if mode == 'absolute':
        ag.position(pos[0], pos[1])
        for i in todo:
            if type(i) == list:
                todo.remove(i)
                break
    times = ag.prompt(text='times', title=title, default='1')
    try:
        for i in range(int(times)):
            playback()
    except ValueError:
        print('Please enter the correct number')
        main()


def recording():
    kb.add_hotkey('p', point)
    kb.add_hotkey('s', sleep)
    kb.add_hotkey('e', stop)
    kb.add_hotkey('l', l_button)
    kb.add_hotkey('r', r_button)
    kb.add_hotkey('m', m_button)
    kb.wait()


def l_button():
    global recorder
    recorder.append('left')


def r_button():
    global recorder
    recorder.append('right')


def m_button():
    global recorder
    recorder.append('middle')


def point():
    global recorder, points
    points.append(ag.position())
    p1 = list(points[-1])
    p2 = list(points[-2])
    recorder.append([p1[0] - p2[0], p1[1] - p2[1]])


def playback():
    time.sleep(10)
    global todo
    for i in todo:
        if type(i) == list:
            ag.moveRel(i[0], i[1])
        elif type(i) == float:
            time.sleep(i)
        elif type(i) == str:
            p = list(ag.position())
            ag.click(p[0], p[1], button=i)


def sleep():
    global recorder, sleep_flag, t
    if sleep_flag:
        t = time.time()
    else:
        recorder.append(time.time() - t)
    sleep_flag = not sleep_flag


def stop():
    global recorder
    print(recorder)
    with open('script.json', 'w') as f:
        json.dump({'data': recorder, 'pos': points[0]}, f)
    sys.exit()


main()
