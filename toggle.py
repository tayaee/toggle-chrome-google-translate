import time

import keyboard
import pyautogui
import pygetwindow as gw
from dotenv import load_dotenv

load_dotenv()
IMAGE_FILE = "google_translate.png"


def run_task():
    clicked = False
    original_mouse_x, original_mouse_y = pyautogui.position()

    win = gw.getActiveWindow()
    if win and ("Chrome" in win.title or "Google" in win.title):
        try:
            region = (win.left, win.top, win.width, win.height)
            location = pyautogui.locateCenterOnScreen(
                IMAGE_FILE,
                confidence=0.8,
                region=region,
            )  # type:ignore
            if location:
                pyautogui.click(location.x, location.y)
                print(f"Clicked Google Translate icon within active window at {location.x}, {location.y}")
                clicked = True
        except Exception as e:
            print(f"No Google Translate icon found from current active window: {e}")

    pyautogui.moveTo(original_mouse_x, original_mouse_y)

    if clicked:
        time.sleep(0.3)
        pyautogui.press("right")
        pyautogui.press("escape")
    else:
        print("[xk4] No action for ctrl-shift-x")


if __name__ == "__main__":
    print("Hotkey: Ctrl + Shift + X")
    print("Exit: Ctrl + C")
    keyboard.add_hotkey("ctrl+shift+x", run_task)
    keyboard.wait()
