import secret
import discord
import pyautogui
import keyboard
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

keyboard.wait("s")

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    old_im = pyautogui.screenshot(region=(168, 559, 1748 - 168, 886 - 559))
    while True:
        print("loop")
        pyautogui.click(1751, 936)
        time.sleep(30)
        im = pyautogui.screenshot(region=(168, 559, 1748 - 168, 886 - 559))
        
        if (rmsdiff(old_im, im) > 2):
            im.save('im.png')
            await client.guilds[0].channels[0].channels[0].send(file=discord.File(r'im.png'))

        old_im = im

client.run(secret.token)