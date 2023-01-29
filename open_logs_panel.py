import pyautogui
import keyboard
import time

while True:
    keyboard.wait("à")

    pyautogui.press('esc')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    pyautogui.press('down')
    pyautogui.press('enter')

    pyautogui.click(716, 259)
    time.sleep(0.5)
    pyautogui.click(1751, 936)