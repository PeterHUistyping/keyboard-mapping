'''
    On macOS, you need to grant permissions for Privacy & Security -> Accessibility + Input Monitoring,
        - the terminal app, 
        - IDE or whatever you are running this script from. 
    Otherwise, it won't be able to control the mouse.

    https://pynput.readthedocs.io/en/latest/limitations.html
    https://pynput.readthedocs.io/en/latest/mouse.html

    sudo /opt/homebrew/bin/python3.10 mirror/keyboard-map.py
'''
import json, os
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener


global MOUSE, LISTEN, PAUSE, KEEP_MOVING
PAUSE, KEEP_MOVING = False, False
MOUSE = Controller()
MOVE_KEYS = ['a', 's', 'd', 'w']
MOVE_KEYS += [c.upper() for c in MOVE_KEYS]


def cust_click(x,y):
    global PAUSE
    if not PAUSE:
        pos = MOUSE.position
        MOUSE.position = (x,y)
        MOUSE.click(Button.left)
        MOUSE.position = pos


def cust_press(x,y):
    global PAUSE
    if not PAUSE:
        pos = MOUSE.position
        MOUSE.position = (x,y)
        MOUSE.press(Button.left)
        MOUSE.position = pos


def cust_release(x,y):
    global PAUSE
    if not PAUSE:
        pos = MOUSE.position
        MOUSE.position = (x,y)
        MOUSE.release(Button.left)
        MOUSE.position = pos


def on_press(key):
    global PAUSE, KEEP_MOVING
    print('{0} pressed at {1}'.format(key, MOUSE.position))
   
    # LISTEN.stop() 
    if key == Key.tab:
        PAUSE = not PAUSE
        print("PAUSE:", PAUSE)
    
    elif key == Key.caps_lock:
        # start or stop the movement
        KEEP_MOVING = not KEEP_MOVING
        print("KEEP_MOVING:", KEEP_MOVING)
        if not KEEP_MOVING:
            cust_press(CENTER_X - DELTA, CENTER_Y)
        else: 
            cust_release(CENTER_X - DELTA, CENTER_Y)

        
    elif key in [Key.space, Key.shift, Key.tab, Key.esc]:
        cust_click(key_binding_json["click"][key.name][0], key_binding_json["click"][key.name][1])

    elif hasattr(key, 'char'): 
        if key.char in MOVE_KEYS:
            '''A S D W, PRESS and HOLD, Release to STOP'''
            if key.char == 'a' or key.char == 'A':
                cust_press(CENTER_X - DELTA, CENTER_Y)
            elif key.char == 'd' or key.char == 'D':
                cust_press(CENTER_X + DELTA, CENTER_Y)
            elif key.char == 's' or key.char == 'S':
                cust_press(CENTER_X, CENTER_Y + DELTA)
            elif key.char == 'w' or key.char == 'W':
                cust_press(CENTER_X, CENTER_Y - DELTA)
        else:
            '''F M J H E for click, case-insensitive'''
            CLICK_CHAR = ['f', 'm', 'j', 'h', 'e', 't', 'c']
            CLICK_CHAR += [c.upper() for c in CLICK_CHAR]
            if key.char in CLICK_CHAR:
                cust_click(key_binding_json["click"][key.char.lower()][0], key_binding_json["click"][key.char.lower()][1])
      

def on_release(key):
    print('{0} release'.format(key))

    BOOL_STOP = False
    if key == Key.space:
        BOOL_STOP = True

    if hasattr(key, 'char'):
        if key.char in MOVE_KEYS:
            BOOL_STOP = True

    if BOOL_STOP:
        MOUSE.release(Button.left)


    # can't use esc because it is the phone 'back' hotkey, at least in snap version
    # if key == Key.esc:
    #     # Stop listener
    #     return False


# Collect events until released
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "archive", "YanYun.json")

    # read from json file
    with open(json_path, 'r') as f:
        key_binding_json = json.load(f)
        print("Loaded JSON data:", key_binding_json)
    

    CENTER_X = key_binding_json["move"]["center"][0]
    CENTER_Y = key_binding_json["move"]["center"][1]
    DELTA = key_binding_json["move"]["delta"]


    with Listener(
            on_press=on_press,
            on_release=on_release,
            ) as LISTEN:
        print("Listener starting...")
        LISTEN.join()

