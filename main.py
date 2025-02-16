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

def press_key(key, sleep=0.3):
    """Simulates pressing the '1' key."""
    pyautogui.press(key)
    print(f"pressed '{key}', sleeping {sleep} seconds")
    time.sleep(sleep)

def focus_and_press_loop(window_title):
    global lastbuff
    global paused
    """Continuously focuses the window and presses '1' every 10 seconds."""
    while True:
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
    window_name = "[#] Rappelz Excellent [#]"
    focus_and_press_loop(window_name)
    print('Press any key to exit')
    input('any key...')
