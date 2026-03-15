'''
    On macOS, you need to grant permissions for Privacy & Security -> Accessibility + Input Monitoring,
        - the terminal app, 
        - IDE or whatever you are running this script from. 
    Otherwise, it won't be able to control the mouse.

    https://pynput.readthedocs.io/en/latest/limitations.html
    https://pynput.readthedocs.io/en/latest/mouse.html

    sudo /opt/homebrew/bin/python3.10 keyboard-map.py
'''
import json, os, time
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener


# global MOUSE, LISTEN, PAUSE, KEEP_MOVING, DISABLE_RELEASE, RECORD_KEYS, key_binding_json_new
PAUSE, KEEP_MOVING, DISABLE_RELEASE, RECORD_KEYS, VERBOSE = False, False, False, False, False
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


def print_with_color(attribute, boolean_value):
    color_code = "\033[92m" if boolean_value else "\033[91m"  # Green for True, Red for False
    reset_code = "\033[0m"
    print(f"\n{color_code}{attribute}: {boolean_value}{reset_code}\n")


def print_help():
    print("---- Help Menu ----")
    print("Press Tab to toggle PAUSE mode.\n\t When PAUSE is on, all key presses will be ignored.")
    print("按Tab键切换暂停模式。\n\t 当暂停模式开启时，所有按键将被忽略。\n")

    print("Press Caps Lock to toggle KEEP_MOVING mode.\n\t When KEEP_MOVING is on, the character will keep moving until you press Caps Lock again.")
    print("按Caps Lock键切换持续移动模式。\n\t 当持续移动模式开启时，角色将持续移动，直到你再次按下Caps Lock键。\n")

    print("Press Space, Shift, Tab, Esc or F M J H E (case-insensitive) to perform a click at the corresponding position defined.")
    print("按空格、Shift、Tab、Esc或F M J H E（不区分大小写）键，在定义的相应位置执行点击。\n")

    print("Press A S D W (case-insensitive) to move in the corresponding direction.")
    print("按A S D W（不区分大小写）键，向相应方向移动。\n")

    #  Press and hold to keep moving, release to stop.
    print("Press F1 to start recording a new position for the next key press.\n\t Press the desired key and move the mouse to the new position. When finished with all changes, press F1 again to save it to the JSON file.")
    print("按F1键开始记录下一个按键的新位置。\n\t 按下想要更改位置的键，并将鼠标移动到新位置。完成所有更改后，再次按F1键将其保存到JSON文件中。\n")

    print("Press F2 to see the summary of all available key bindings and their positions.")
    print("按F2键查看所有可用按键绑定及其位置的摘要。\n")

    print("Press F3 to see this help menu again.")
    print("按F3键再次查看此帮助菜单。\n")

    print("Press F4 to toggle VERBOSE mode.\n\t When VERBOSE is on, it will print the key presses and releases along with the mouse position.")
    print("按F4键切换详细模式。\n\t 当详细模式开启时，它将打印按键和释放以及鼠标位置。\n")
    print("---- Help Menu ----")


def print_summary(key_binding_json):
    print("---- Available Key Bindings ----")
    for action, bindings in key_binding_json.items():
        print(f"{action}:")
        for key_name, pos in bindings.items():
            print(f"  {key_name}: {pos}")
    print("---- Available Key Bindings ----")


def on_press(key):
    global PAUSE, KEEP_MOVING, DISABLE_RELEASE, HISTORY_CHAR, RECORD_KEYS, key_binding_json, key_binding_json_new, json_path, VERBOSE
    pos_x, pos_y = MOUSE.position
    if VERBOSE:
        print('{0} pressed at ({1}, {2})' .format(key, int(pos_x), int(pos_y))) 

    # LISTEN.stop() 
    if key == Key.tab:
        PAUSE = not PAUSE
        print_with_color("PAUSE", PAUSE)
    
    elif key == Key.caps_lock:
        # start or stop the movement
        KEEP_MOVING = not KEEP_MOVING
        print_with_color("KEEP_MOVING", KEEP_MOVING)
        if not KEEP_MOVING:
            cust_press(CENTER_X - DELTA, CENTER_Y, reset_pos=True)
        else: 
            cust_release(CENTER_X - DELTA, CENTER_Y)

    elif key in [Key.space, Key.shift, Key.tab, Key.esc]:
        cust_click(key_binding_json["click"][key.name][0], key_binding_json["click"][key.name][1])
        if RECORD_KEYS:
            key_binding_json_new["click"][key.name] = [int(pos_x), int(pos_y)]

    elif hasattr(key, 'char'): 
        if key.char == HISTORY_CHAR and False:
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
    
    # start recording a new position for json file.
    elif key == Key.f1:
        print("Recording position for F1 key...")
        RECORD_KEYS = not RECORD_KEYS
        if RECORD_KEYS:
            print("Move the mouse to the desired positions and press F1 again to save it.")
            key_binding_json_new = key_binding_json.copy()
        else:
            with open(json_path, 'w') as f:
                json.dump(key_binding_json_new, f, indent=4)

            json_path_backup = os.path.join(current_dir, "archive", "YanYun-backup" + "_" + str(time.time()) + ".json")
            with open(json_path_backup, 'w') as f:
                json.dump(key_binding_json_new, f, indent=4)
            key_binding_json = key_binding_json_new.copy()
            print("Saved recorded positions to JSON file.")
    
    # print the summary of all available key bindings
    elif key == Key.f2:
        print_summary(key_binding_json) 

    elif key == Key.f3:
        print_help()
    
    elif key == Key.f4:
        VERBOSE = not VERBOSE
        print_with_color("VERBOSE", VERBOSE)


def on_release(key):
    global DISABLE_RELEASE
    if VERBOSE:
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
        print("Reading from existing key binding JSON file. DONE!")
        # print("Loaded JSON data:", key_binding_json)

    CENTER_X = key_binding_json["move"]["center"][0]
    CENTER_Y = key_binding_json["move"]["center"][1]
    DELTA = key_binding_json["move"]["delta"]


    with Listener(
            on_press=on_press,
            on_release=on_release,
            ) as LISTEN:
        print("✨ 𝓦𝓮𝓵𝓬𝓸𝓂𝓮 ✨ to keyboard-mouse binding ────୨ৎ────")
        print("Listening to keyboard events... Press F3 for help.")
        LISTEN.join()

