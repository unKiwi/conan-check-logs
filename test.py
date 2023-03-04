from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    return False

with Listener(on_click=on_click) as listener:
    listener.join()