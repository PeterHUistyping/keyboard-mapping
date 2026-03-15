# Keyboard mapping tool for scrcpy

This tool allows you to create custom keyboard mappings for scrcpy, enabling you to control your Android device using your keyboard.
  - e.g. for [scrcpy](https://github.com/genymobile/scrcpy), which is a screen copying, mirroring and control tool for Android devices, or other tasks that require keyboard input to control an Android device.

## Features
- Create custom keyboard mappings for scrcpy (F1 key).
- Save and load keyboard mapping configurations (F2 key).
- Help menu for instructions (F3 key).
- Debugging mode to print key events (F4 key).
- Keep moving in the same direction (Cap Lock key to toggle).
- Pause the keyboard mapping tool (Tab key to toggle).

The current version supports emulating only a single key press.
- Features tested on macOS full screen mode.

## Usage

1. Clone the repository.
2. Install the required dependencies from `requirements.txt` or refer to `scrcpy_install.sh`.
3. Allow system permissions of Privacy & Security -> Accessibility + Input Monitoring for the terminal and python IDEs.
4. Update the python path in `scrcpy.sh`.
5. Run the tool and follow the help instructions to create your keyboard mapping.


## Example configuration

```json
"move":{
    "center": [280, 600],
    "delta": 50
},
"click": {
    "space": [1348, 587],
    "shift": [1195, 708],
    "esc": [1338, 168],
    "f": [946, 432],
    "m": [200, 220],
    "j": [115, 322],
    "h": [110, 520],
    "t": [105, 651],
    "c": [108, 722],
    "p": [718, 161],
    "1": [1300, 259],
    "2": [1314, 318],
    "3": [1210, 604],
    "4": [1224, 479],
    "5": [1318, 474],
    "6": [1126, 520],
    "7": [1083, 413],
    "e": [1072, 611],
    "q": [1058, 709],
    "v": [108, 581]
}
```

![Where winds meet-Yanyun](./archive/YanYun.png)

