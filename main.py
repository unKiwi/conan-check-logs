import secret
import discord
import pyautogui
import time

from PIL import ImageChops
import math, operator
from functools import reduce

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1]))

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    oldLogs = pyautogui.screenshot(region=(168, 559, 1748 - 168, 886 - 559))
    while True:
        print("loop")

        pyautogui.click(1751, 936) # click submit button

        destroyMessageRegion = pyautogui.locateOnScreen('search_screen_en.png', region=(488, 560, 1743 - 488, 882 - 560), confidence=0.9)
        if (destroyMessageRegion):
            # destroy message found
            im = pyautogui.screenshot(region=(168, 559, 1748 - 168, 886 - 559))
            if (rmsdiff(oldLogs, im) > 2):
                im.save('last_logs.png')
                await client.guilds[0].channels[0].channels[0].send(file=discord.File(r'last_logs.png'))

            oldLogs = im

        time.sleep(20)

client.run(secret.token)
