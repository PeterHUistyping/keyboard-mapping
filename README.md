# Keyboard mapping tool for scrcpy

- [scrcpy](https://github.com/genymobile/scrcpy) is a screen copying, mirroring and control tool for Android devices.
- This tool allows you to create custom keyboard mappings for scrcpy, enabling you to control your Android device using your keyboard.

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
