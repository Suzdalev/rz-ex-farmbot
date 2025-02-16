import time
import pygetwindow as gw
import pyautogui
import random
import keyboard

def focus_window(window_title):
    """Focuses the specified window."""
    window = gw.getWindowsWithTitle(window_title)
    if window:
        window = window[0]
        if not window.isActive:
            window.activate()
        print(f"Focused on window: {window_title}")
        return True
    else:
        print(f"Window '{window_title}' not found.")
        return False

def press_key(key):
    """Simulates pressing the '1' key."""
    pyautogui.press(key)
    print(f"Pressed key {key}")

def focus_and_press_loop(window_title):
    """Continuously focuses the window and presses '1' every 10 seconds."""
    while True:
        try:
            if focus_window(window_title):
                press_key('1')
                time.sleep(0.4)
                press_key('2')
                time.sleep(0.4)
                press_key('1')
                time.sleep(0.4)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(random.randint(0,2))

if __name__ == "__main__":
    window_name = "[#] Rappelz Excellent [#]"
    focus_and_press_loop(window_name)
