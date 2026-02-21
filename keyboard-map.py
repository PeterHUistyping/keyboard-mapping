'''
    On macOS, you need to grant permissions for Privacy & Security -> Accessibility + Input Monitoring,
        - the terminal app, 
        - IDE or whatever you are running this script from. 
    Otherwise, it won't be able to control the mouse.

    https://pynput.readthedocs.io/en/latest/limitations.html
    https://pynput.readthedocs.io/en/latest/mouse.html

    sudo /opt/homebrew/bin/python3.10 mirror/keyboard-map.py
'''
import json, os, time
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener


# global MOUSE, LISTEN, PAUSE, KEEP_MOVING, DISABLE_RELEASE, RECORD_KEYS, key_binding_json_new
PAUSE, KEEP_MOVING, DISABLE_RELEASE, RECORD_KEYS = False, False, False, False
key_binding_json, key_binding_json_new = {}, {}
HISTORY_CHAR = '-1'
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


def cust_press(x,y, reset_pos=True):
    global PAUSE
    if not PAUSE:
        pos = MOUSE.position
        MOUSE.position = (x,y)
        MOUSE.press(Button.left)
        if reset_pos:
            MOUSE.position = pos


def cust_release(x,y):
    global PAUSE
    if not PAUSE:
        pos = MOUSE.position
        MOUSE.position = (x,y)
        MOUSE.release(Button.left)
        MOUSE.position = pos


def on_press(key):
    global PAUSE, KEEP_MOVING, DISABLE_RELEASE, HISTORY_CHAR, RECORD_KEYS, key_binding_json, key_binding_json_new, json_path
    pos_x, pos_y = MOUSE.position
    print('{0} pressed at ({1}, {2})' .format(key, int(pos_x), int(pos_y))) 

    # LISTEN.stop() 
    if key == Key.tab:
        PAUSE = not PAUSE
        print("PAUSE:", PAUSE)
    
    elif key == Key.caps_lock:
        # start or stop the movement
        KEEP_MOVING = not KEEP_MOVING
        print("KEEP_MOVING:", KEEP_MOVING)
        if not KEEP_MOVING:
            cust_press(CENTER_X - DELTA, CENTER_Y, reset_pos=True)
        else: 
            cust_release(CENTER_X - DELTA, CENTER_Y)

    elif key in [Key.space, Key.shift, Key.tab, Key.esc]:
        cust_click(key_binding_json["click"][key.name][0], key_binding_json["click"][key.name][1])
        if RECORD_KEYS:
            key_binding_json_new["click"][key.name] = [int(pos_x), int(pos_y)]

    elif hasattr(key, 'char'): 
        if key.char == HISTORY_CHAR:
            DISABLE_RELEASE = True
        else:
            DISABLE_RELEASE = False
        
        if key.char in MOVE_KEYS:
            '''A S D W, PRESS and HOLD, Release to STOP'''
            if key.char == 'a' or key.char == 'A':
                cust_press(CENTER_X - DELTA, CENTER_Y, reset_pos=False) 
            elif key.char == 'd' or key.char == 'D': 
                cust_press(CENTER_X + DELTA, CENTER_Y, reset_pos=False)
            elif key.char == 's' or key.char == 'S':
                cust_press(CENTER_X, CENTER_Y + DELTA, reset_pos=False)
            elif key.char == 'w' or key.char == 'W':
                cust_press(CENTER_X, CENTER_Y - DELTA, reset_pos=False)
            
            if RECORD_KEYS:
                key_binding_json_new["move"][key.char.lower()] = [int(pos_x), int(pos_y)]
        else:
            '''F M J H E for click, case-insensitive'''
            # CLICK_CHAR = ['f', 'm', 'j', 'h', 'e', 't', 'c']
            # find CLICK_CHAR from single char keys in key_binding_json["click"]
            CLICK_CHAR = [k for k in key_binding_json["click"].keys() if len(k) == 1]
            CLICK_CHAR += [c.upper() for c in CLICK_CHAR]
            if key.char in CLICK_CHAR:
                cust_click(key_binding_json["click"][key.char.lower()][0], key_binding_json["click"][key.char.lower()][1])

            if RECORD_KEYS:
                key_binding_json_new["click"][key.char.lower()] = [int(pos_x), int(pos_y)]
        HISTORY_CHAR = key.char
    
    elif key == Key.f1:
        # start recording a new position for json file.
        print("Recording position for F1 key...")
        RECORD_KEYS = not RECORD_KEYS
        if RECORD_KEYS:
            print("Move the mouse to the desired positions and press F1 again to save it.")
            key_binding_json_new = key_binding_json.copy()
        else:
            with open(json_path, 'w') as f:
                json.dump(key_binding_json_new, f, indent=4)

            json_path = os.path.join(current_dir, "archive", "YanYun-backup" + "_" + str(time.time()) + ".json")
            with open(json_path, 'w') as f:
                json.dump(key_binding_json, f, indent=4)
            key_binding_json = key_binding_json_new.copy()
            print("Saved recorded positions to JSON file.")


def on_release(key):
    global DISABLE_RELEASE
    print('{0} release'.format(key))

    BOOL_STOP = False
    if key == Key.space:
        BOOL_STOP = True

    if hasattr(key, 'char'):
        if key.char in MOVE_KEYS:
            BOOL_STOP = True

    if BOOL_STOP:
        if not DISABLE_RELEASE:
            MOUSE.release(Button.left)
        else:
            print("Keep pressing the key until a new key is pressed.")


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

