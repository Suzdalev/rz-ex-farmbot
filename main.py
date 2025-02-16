import os
import time
import datetime
import pygetwindow as gw
import pyautogui
import random
import keyboard
import easyocr
import numpy as np
from PIL import Image
from threading import Thread
import mss
import mss.tools

paused = False
lastbuff = 0
num_to_click = None

# Target RGB color and threshold for filtering
TARGET_COLOR = (255, 234, 0)  # Yellow text color
THRESHOLD = 1  # Allowed color deviation
reader = easyocr.Reader(['en'])
def filter_by_color(image_path, target_color=TARGET_COLOR, threshold=THRESHOLD):
    """ Keeps only pixels near the target color and turns others black. """
    image = Image.open(image_path).convert("RGB")
    data = np.array(image)

    # Compute color distance to target color
    r, g, b = target_color
    mask = np.sqrt((data[..., 0] - r) ** 2 + (data[..., 1] - g) ** 2 + (data[..., 2] - b) ** 2) < threshold

    # Create a new black background image
    filtered_data = np.zeros_like(data)  # Black background
    filtered_data[mask] = target_color  # Keep only yellow text

    # Save and return filtered image
    filtered_image = Image.fromarray(filtered_data.astype(np.uint8))
    filtered_image_path = "filtered_image.png"
    filtered_image.save(filtered_image_path)
    return filtered_image_path

def recognize_text(image_path):
    global reader
    result = reader.readtext(image_path)
    return result

def get_number_to_click():
    input_image = "screenshot.png"  # Change to your image file name
    filtered_path = filter_by_color(input_image)
    text_results = recognize_text(filtered_path)

    print("Recognized Text:")
    for bbox, text, confidence in text_results:
        if "".join(text).__contains__('Click on the number'):
            print(f"FOUND: {text}")
            number= text.split()[-1]
            for ch in number:
                try:
                    num = int(ch)
                    number = num
                    return number
                except ValueError:
                    continue

def screenshot_checker():
    global num_to_click
    while True:
        os.rename("screenshot.png",f"scr{datetime.datetime.now().isoformat().replace(':', '-').replace('.','')}.png")
        with mss.mss() as sct:
            screenshot = sct.shot(output='screenshot.png')
        num_to_click = get_number_to_click()
        if num_to_click is not None:
            print("No macro numbers detected")
        time.sleep(25)


def focus_window(window_title):
    """Focuses the specified window."""
    window = gw.getWindowsWithTitle(window_title)
    if window:
        window = window[0]
        if not window.isActive:
            window.activate()
        #print(f"Focused on window: {window_title}")
        return True
    else:
        print(f"Window '{window_title}' not found.")
        return False

def press_key(key, sleep=0.3):
    """Simulates pressing the '1' key."""
    pyautogui.press(key)
    #print(f"pressed '{key}', sleeping {sleep} seconds")
    time.sleep(sleep)

def press_shift_key(key, sleep=0.3):
    """Simulates pressing the '1' key."""
    with pyautogui.hold('shift'):
        pyautogui.press(key)
    print(f"pressed 'Shift+{key}', sleeping {sleep} seconds")
    time.sleep(sleep)

def focus_and_press_loop(window_title):
    global lastbuff
    global paused
    global num_to_click
    """Continuously focuses the window and presses '1' every 10 seconds."""
    while True:
        print(f"Macro number: {num_to_click}")
        try:
            if keyboard.is_pressed('p'):
                paused = not paused
                if paused:
                    print("Bot is paused")
                    time.sleep(5)
                else:
                    print("Bot continues ")
                time.sleep(0.2)
            if paused:
                continue

            if num_to_click is not None:
                # Antimacro
                with mss.mss() as sct:
                    screenshot = sct.shot(output='before_macro.png')
                time.sleep(1)
                press_shift_key(num_to_click)
                time.sleep(1)
                with mss.mss() as sct:
                    screenshot = sct.shot(output='after_macro.png')
                num_to_click = None

            if focus_window(window_title) and not paused:
                press_key('1')
                press_key('2')

            # check buffs
            if time.time() - lastbuff > 20*60.0:# 20 minutes
                for number in range(4,9):
                    press_key(str(number), 2.0)
                lastbuff = time.time()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(random.randint(0,2))

if __name__ == "__main__":

    screenshot_thr = Thread(target=screenshot_checker, daemon=True)
    screenshot_thr.start()

    window_name = "[#] Rappelz Excellent [#]"
    focus_and_press_loop(window_name)
    print('Press any key to exit')
    input('any key...')
