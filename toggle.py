import os
import time
import tkinter as tk
from tkinter import simpledialog

import cv2
import keyboard
import mss
import numpy as np
import psutil
import pyautogui
import pygetwindow as gw
from dotenv import load_dotenv, set_key
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


log("Script starting...")

load_dotenv()
IMAGE_FILE = "google_translate.png"
ENV_FILE = ".env"
current_hotkey = os.getenv("HOTKEY", "ctrl+shift+x")


def kill_previous_instances():
    log("Cleaning up old instances...")
    current_pid = os.getpid()
    parent_pid = psutil.Process(current_pid).ppid()

    count = 0
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmd = proc.info.get("cmdline")
            if cmd and any("toggle.py" in s for s in cmd):
                pid = proc.info["pid"]
                if pid == current_pid or pid == parent_pid:
                    continue

                log(f"Terminating target PID {pid}...")
                p = psutil.Process(pid)
                p.terminate()
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    log(f"Cleanup done. {count} instances removed.")


NEEDLE_IMG = cv2.imread(IMAGE_FILE)
last_win_state = None  # (left, top, width, height)
last_target_loc = None  # (actual_x, actual_y)

pyautogui.PAUSE = 0.05


def run_task():
    global last_win_state, last_target_loc

    start_time = time.time()
    log(">>> Hotkey Triggered <<<")

    try:
        curr_x, curr_y = pyautogui.position()
        win = gw.getActiveWindow()

        if not win or not ("Chrome" in win.title or "Google" in win.title):
            log("Not in Chrome.")
            return

        current_state = (win.left, win.top, win.width, win.height)
        target_loc = None

        # [Tuning 1] If the window state is the same as before, use the saved coordinates immediately.
        if last_win_state == current_state and last_target_loc:
            target_loc = last_target_loc
            log("Cache Hit! (Instant execution)")
        else:
            # [Tuning 2] If the state is different (window moved/resized), search only the top area
            with mss.mss() as sct:
                monitor = {
                    "top": win.top,
                    "left": win.left,
                    "width": win.width,
                    "height": min(win.height, 150),
                }

                img_src = sct.grab(monitor)
                haystack = cv2.cvtColor(np.array(img_src), cv2.COLOR_BGRA2BGR)

                res = cv2.matchTemplate(haystack, NEEDLE_IMG, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)

                if max_val >= 0.8:
                    h, w = NEEDLE_IMG.shape[:2]
                    # 실제 스크린 좌표 계산
                    target_loc = (
                        max_loc[0] + monitor["left"] + w / 2,
                        max_loc[1] + monitor["top"] + h / 2,
                    )
                    # 캐시 갱신
                    last_win_state = current_state
                    last_target_loc = target_loc
                    log(f"Cache Updated (Search took: {time.time() - start_time:.4f}s)")

        # [Tuning 3] Execution Unit Optimization
        if target_loc:
            pyautogui.click(x=target_loc[0], y=target_loc[1])
            time.sleep(0.15)
            pyautogui.moveTo(curr_x, curr_y)
            pyautogui.press("right")
            pyautogui.press("escape")

            elapsed = time.time() - start_time
            log(f"Action Success. Total: {elapsed:.4f}s")
        else:
            log(f"Icon not found inside window. ({time.time() - start_time:.4f}s)")

    except Exception as e:
        log(f"Task Error: {e}")


def setup_hotkey(new_hotkey=None):
    global current_hotkey
    if new_hotkey:
        current_hotkey = new_hotkey
        set_key(ENV_FILE, "HOTKEY", current_hotkey)

    log(f"Registering: {current_hotkey}")
    try:
        keyboard.unhook_all()
        keyboard.add_hotkey(current_hotkey, run_task, suppress=False)
        log("Hotkey Ready.")
    except Exception as e:
        log(f"Hotkey Failed: {e}")


def change_hotkey_prompt(icon):
    root = tk.Tk()
    root.withdraw()
    new_key = simpledialog.askstring(
        "Settings", "Enter Hotkey:", initialvalue=current_hotkey
    )
    if new_key:
        setup_hotkey(new_key)
    root.destroy()


def on_quit(icon, item):
    log("Quitting...")
    icon.stop()
    os._exit(0)


def create_image():
    img = Image.new("RGB", (64, 64), color=(66, 133, 244))
    d = ImageDraw.Draw(img)
    d.rectangle([16, 16, 48, 48], fill=(255, 255, 255))
    return img


if __name__ == "__main__":
    try:
        kill_previous_instances()

        menu = Menu(
            MenuItem(
                lambda item: f"Key: {current_hotkey}",
                lambda: None,
                enabled=False,
            ),
            MenuItem("Change Hotkey", change_hotkey_prompt),
            MenuItem("Quit", on_quit),
        )
        icon = Icon(
            "GToggle",
            create_image(),
            "Toggle Language (Google Translate)",
            menu,
        )

        setup_hotkey()

        log("Entering main loop (Ready for hotkey)...")
        icon.run()

    except Exception as e:
        log(f"CRITICAL ERROR: {e}")
        time.sleep(10)
