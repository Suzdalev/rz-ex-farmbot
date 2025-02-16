import time
import pygetwindow as gw
import pyautogui
import random
import keyboard

paused = False
lastbuff = 0
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
            if focus_window(window_title) and not paused:
                press_key('1')
                time.sleep(0.4)
                press_key('2')
                time.sleep(0.4)
                press_key('1')
                time.sleep(0.4)

            # check buffs
            if time.time() - lastbuff > 20*60.0:# 20 minutes
                press_key('5')
                time.sleep(2)
                press_key('6')
                time.sleep(2)
                press_key('7')
                time.sleep(2)
                press_key('8')
                time.sleep(2)
                press_key('9')
                time.sleep(2)
                press_key('0')
                time.sleep(2)
                lastbuff = time.time()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(random.randint(0,2))

if __name__ == "__main__":
    window_name = "[#] Rappelz Excellent [#]"
    focus_and_press_loop(window_name)
    print('Press any key to exit')
    input('any key...')
