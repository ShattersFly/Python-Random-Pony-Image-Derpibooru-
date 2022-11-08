import ctypes.wintypes
import os
import random
import platform
import time
import webbrowser
import win10toast_click

from derpibooru import Search, query
from win11toast import toast

CSIDL_PERSONAL = 5  # My Documents
SHGFP_TYPE_CURRENT = 0  # Get current, not default value

buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
configFile = buf.value + '\\randomponyconfig.ini'

s1 = "You're running this program for the first time\n"
s2 = "Config file generated at: "
s3 = "Default time interval per image - 20 minutes, to change it - change value in the config\n"
s4 = "To exit program: kill 'imagenotification.exe' in task manager\n"
s5 = "WARNING: Windows notifications must be enabled/allowed to program to work"

defaultTags = "safe, !butt, !sfm, !equestria girls, !caption, !screencap, !traditional art, !photo, !bondage, !fetish, !spread legs, !blender"
                    # ^ this specific tagged images can come out as a result and are usually either low quality or not-so-safe

class Error:
    couldntCreate = 'Something wrong with the config file, proceeding with default values'
    w1 = "Config missing or it's structure corrupt, proceeding with default values\n"
    w2 = "Generate new config by removing the old one and/or launching app again"
    corruptConfig = w1+w2
    couldntGet = "Couldn't get image, internet or script issue, ignoring current image"

try:
    if not os.path.isfile(configFile):
        with open(configFile, 'w') as f:
            f.write('interval_minutes=20\n'+'tags='+defaultTags)
            f.close()
        ctypes.windll.user32.MessageBoxW(0,'{}{}{}{}{}{}'.format(s1,s2,buf.value+'\n',s3,s4,s5), 'Random Pony 4 U: Notice', 0)
    else:
        try:
            with open(configFile) as config:
                lines = config.readlines()
                intervaloftime = 60 * lines[0].replace('interval_minutes=','')
                defaultTags = lines[1].replace('tags=','')
        except Exception:
            ctypes.windll.user32.MessageBoxW(0, Error.corruptConfig, 'Random Pony 4 U: Error', 0)
except Exception:
    ctypes.windll.user32.MessageBoxW(0, Error.couldntCreate, 'Random Pony 4 U: Error', 0)
    pass


def checkFile():    # default to 20 minutes if config file was removed during program running
    try:
        if os.path.isfile(configFile):
            with open(configFile) as config:
                intervaloftime = 60 * int(config.readlines()[0].replace('interval_minutes=',""))
        else:
            intervaloftime = 1200
        return intervaloftime
    except Exception:
        ctypes.windll.user32.MessageBoxW(0, Error.corruptConfig, 'Random Pony 4 U: Error', 0)
        intervaloftime = 1200
        return intervaloftime

def checkTags(dt):
    defaultTags = dt
    try:
        if os.path.isfile(configFile):
            with open(configFile) as config:
                newTags = config.readlines()[1].replace('tags=',"")
        return newTags
    except Exception:
        ctypes.windll.user32.MessageBoxW(0, Error.corruptConfig, 'Random Pony 4 U: Error', 0)
        return defaultTags

score = [35, 150, 200, 300, 500, 700]
q = {
    checkTags(defaultTags),
    query.score >= random.choice(score)
}

seenList = []


def open_url(what):
    try:
        webbrowser.open_new(what)
    except:
        pass


def getNewWallpapers():
    try:
        wallpapers = [image for image in Search().query(*q)]
        randomimage = random.choice(wallpapers).url
        seenList.append(randomimage)
        while randomimage == seenList.index(randomimage): #attempt not to show same images too often
            randomimage = random.choice(wallpapers).url
        if len(seenList) >= 5:
            seenList.pop(len(seenList) - 1)
    except Exception:
        randomimage = ''
        ctypes.windll.user32.MessageBoxW(0, Error.couldntGet, 'Random Pony 4 U: Error', 0)
    return randomimage


image = getNewWallpapers()
notif = win10toast_click.ToastNotifier()

buttons = [
    {'activationType': 'protocol', 'arguments': image, 'content': 'Open'}
]
try:
    if platform.platform().find('Windows-7') == -1 and image != '':
        toast('Random Pony 4 U', "Here's your first image", image=image, buttons=buttons, duration='long',
              on_click=image)
    elif image != '':
        notif.show_toast('Random Pony 4 U', 'Your first pony arrived! Click to open', duration=25,
                         callback_on_click=open_url(image))
except Exception:
    pass

while True:
    time.sleep(checkFile())
    image = getNewWallpapers()
    try:
        if platform.platform().find('Windows-7') == -1 and image != '':
            toast('Random Pony 4 U', "Here's your pony", image=image, buttons=buttons, duration='long', on_click=image)
        elif image != '':
            notif.show_toast('Random Pony 4 U', 'Your pony arrived! Click to open', duration=25,
                             callback_on_click=open_url(image))
    except Exception:
        pass
