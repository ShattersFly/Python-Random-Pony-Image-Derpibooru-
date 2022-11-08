from win11toast import toast
from derpibooru import Search, query
import random, win10toast_click, time, os, ctypes.wintypes, ctypes, sys, webbrowser

CSIDL_PERSONAL = 5       # My Documents
SHGFP_TYPE_CURRENT = 0   # Get current, not default value

buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

if not os.path.isfile(buf.value+'\\randomponyconfig.ini'):
    with open(buf.value+'\\randomponyconfig.ini', 'w') as f:
        f.write('20')
    ctypes.windll.user32.MessageBoxW(0, 'This is your first time running this program\nConfig file generated at: {}\nDefault inverval per image is 20 minutes, to change that - change value in the config\nTo stop the program kill its process in task manager\nIn order for this program to work - windows notifications must be enabled/allowed'.format(buf.value),'Random Pony 4 U: Notice', 0)

score = [35,150,200,300,500,700]
q = {
  "safe, !butt, !sfm, !equestria girls, !caption, !screencap, !traditional art, !photo, !bondage, !fetish, !spread legs, !blender",
  query.score >= random.choice(score)
}

seenList = []

def checkFile():
    if os.path.isfile(buf.value+'\\randomponyconfig.ini'):
        with open(buf.value + '\\randomponyconfig.ini') as nameOftheOpenedFile:
            intervaloftime = 60 * int(nameOftheOpenedFile.read())
    else:
        intervaloftime = 1200
    return intervaloftime

def open_url(what):
    try:
        webbrowser.open_new(what)
    except:
        pass

def getNewWallpapers():
    wallpapers = [image for image in Search().query(*q)]
    randomimage = random.choice(wallpapers).url
    seenList.append(randomimage)
    while randomimage == seenList.index(randomimage):
        randomimage = random.choice(wallpapers).url
    seenList.append(randomimage)
    if len(seenList) >= 5:
        seenList.pop(len(seenList)-1)
    return randomimage
image = getNewWallpapers()
notif = win10toast_click.ToastNotifier()

buttons = [
    {'activationType': 'protocol', 'arguments': image, 'content': 'Open'}
]
try:
    if int(list(sys.getwindowsversion())[0]) != 6:
        toast('Random Pony 4 U', "Here's your first image", image=image, buttons=buttons, duration='long', on_click=image)
    else:
        notif.show_toast('Random Pony 4 U', 'Your first pony arrived! Click to open', duration=25, callback_on_click=open_url(image))
except Exception:
    pass

UniverseExists = True
while UniverseExists == True:
        time.sleep(checkFile())
        image = getNewWallpapers()
        try:
            if int(list(sys.getwindowsversion())[0]) != 6:
                toast('Random Pony 4 U', "Here's your pony", image=image, buttons=buttons, duration='long', on_click=image)
            else:
                notif.show_toast('Random Pony 4 U', 'Your pony arrived! Click to open', duration=25, callback_on_click=open_url(image))
        except Exception:
            pass
