import secret
import discord
import pyautogui
import time
import threading
import asyncio
from pynput.mouse import Listener

from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

import pytesseract
pytesseract.pytesseract.tesseract_cmd ='C:\Program Files (x86)\Tesseract-OCR\\tesseract.exe'

def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]

def on_click(x, y, button, pressed):
    if pressed:
        return False
    
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

# init conf
strToFind = pyautogui.prompt(text='Text to locate' , default=" was destroyed by ")
nbErrorPossible = int(pyautogui.prompt(text='Max syntax error' , default="5"))
nbSecondsToWait = int(pyautogui.prompt(text='Number of seconds to wait before new submit' , default="20"))

pyautogui.alert(text='After close this window, click first corner of the area where you want to find the text then the second corner and then the submit button')

with Listener(on_click=on_click) as listener:
    listener.join()
firstCorner = pyautogui.position()

with Listener(on_click=on_click) as listener:
    listener.join()
secondCorner = pyautogui.position()

with Listener(on_click=on_click) as listener:
    listener.join()
submitButton = pyautogui.position()

x1 = firstCorner.x if firstCorner.x < secondCorner.x else secondCorner.x
x2 = secondCorner.x if firstCorner.x < secondCorner.x else firstCorner.x
y1 = firstCorner.y if firstCorner.y < secondCorner.y else secondCorner.y
y2 = secondCorner.y if firstCorner.y < secondCorner.y else firstCorner.y

# trigger function
def trigger():
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

        await client.guilds[0].channels[0].channels[0].send(file=discord.File(r'last_logs.png'))

    client.run(secret.token)

while True:
    im = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    result = pytesseract.image_to_string(im)

    textsTested = []
    resLevenshtein = []
    for i in range(0, len(result) - len(strToFind)):
        textToTest = result[i:i+len(strToFind)]
        textsTested.append(textToTest)
        resLevenshtein.append(levenshtein(textToTest, strToFind))

    index_min = 0
    for i in range(1, len(resLevenshtein)):
        if resLevenshtein[i] < resLevenshtein[index_min]:
            index_min = i
    
    if (min(resLevenshtein) <= nbErrorPossible):
        # destroy message found
        print('\033[91m' + ' "' + strToFind + '" was find' + '\033[0m')
        im.save('last_logs.png')
        trigger()
    else:
        print('Best match: ' + textsTested[index_min])

    lastMousePos = pyautogui.position()
    pyautogui.click(submitButton) # click submit button
    pyautogui.moveTo(lastMousePos) # come back

    time.sleep(nbSecondsToWait)