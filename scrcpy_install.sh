brew install scrcpy
brew install --cask android-platform-tools

adb devices

# commit as a macOS app via pyinstaller
pip install pyinstaller
# --windowed: no console, only the app window
pyinstaller --onefile \
  --add-data "archive/YanYun.json:archive" \
  keyboard-map.py
pyinstaller main.spec