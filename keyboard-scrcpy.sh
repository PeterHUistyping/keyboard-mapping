# sudo bash scrcpy.sh
sudo -v

read -p "Open scrcpy? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # key bindings & scrcpy
    /opt/homebrew/bin/python3.10 keyboard-map.py & scrcpy -d > /dev/null 2>&1
else
    /opt/homebrew/bin/python3.10 keyboard-map.py
fi 
