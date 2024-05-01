import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import time


def focus_window_by_title(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]
        if window:
            if window.isMinimized:
                window.restore()
            window.activate()
            # Give some time for the window to come to the foreground
            time.sleep(1)
            return window
    except IndexError:
        print("Window not found. Make sure the window title is correct.")
        return None


def capture_window(window):
    x, y, w, h = window.left, window.top, window.width, window.height
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Position clicked:", x, y)


def main():
    window_title = "Teclado"
    window = focus_window_by_title(window_title)
    if window:
        img = capture_window(window)
        cv2.namedWindow("Setup Helper")
        cv2.setMouseCallback("Setup Helper", mouse_callback)
        while True:
            cv2.imshow("Setup Helper", img)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
    else:
        print("Failed to find the window titled:", window_title)


if __name__ == '__main__':
    main()
