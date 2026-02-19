import time
import os
import psutil
import keyboard
import pyautogui
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem
from dotenv import load_dotenv, set_key
import sys

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
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = proc.info.get('cmdline')
            if cmd and any("toggle.py" in s for s in cmd):
                pid = proc.info['pid']
                if pid == current_pid or pid == parent_pid:
                    continue
                
                log(f"Terminating target PID {pid}...")
                p = psutil.Process(pid)
                p.terminate()
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    log(f"Cleanup done. {count} instances removed.")

def run_task():
    log(">>> Hotkey Triggered <<<")
    try:
        curr_x, curr_y = pyautogui.position()
        win = gw.getActiveWindow()
        if win and ("Chrome" in win.title or "Google" in win.title):
            region = (win.left, win.top, win.width, win.height)
            loc = pyautogui.locateCenterOnScreen(IMAGE_FILE, confidence=0.8, region=region)
            if loc:
                pyautogui.click(loc.x, loc.y)
                pyautogui.moveTo(curr_x, curr_y)
                time.sleep(0.3)
                pyautogui.press("right")
                pyautogui.press("escape")
                log("Action Success.")
            else:
                log("Icon not found.")
        else:
            log("Not in Chrome.")
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
    new_key = simpledialog.askstring("Settings", "Enter Hotkey:", initialvalue=current_hotkey)
    if new_key:
        setup_hotkey(new_key)
    root.destroy()

def on_quit(icon, item):
    log("Quitting...")
    icon.stop()
    os._exit(0)

def create_image():
    img = Image.new('RGB', (64, 64), color=(66, 133, 244))
    d = ImageDraw.Draw(img)
    d.rectangle([16, 16, 48, 48], fill=(255, 255, 255))
    return img

if __name__ == "__main__":
    try:
        kill_previous_instances()

        menu = Menu(
            MenuItem(lambda item: f"Key: {current_hotkey}", lambda: None, enabled=False),
            MenuItem("Change Hotkey", change_hotkey_prompt),
            MenuItem("Quit", on_quit)
        )
        icon = Icon("GToggle", create_image(), "Toggle Language (Google Translate)", menu)

        setup_hotkey()

        log("Entering main loop (Ready for hotkey)...")
        icon.run()

    except Exception as e:
        log(f"CRITICAL ERROR: {e}")
        time.sleep(10)