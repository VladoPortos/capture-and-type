import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()


def wait_and_focus_window(title, timeout=60):
    start_time = time.time()
    while True:
        window = gw.getWindowsWithTitle(title)
        if window:
            window = window[0]
            if window.isMinimized:
                window.restore()
            window.activate()
            pyautogui.click(window.left + window.width // 2,
                            window.top + window.height // 2)
            return window
        elif time.time() - start_time > timeout:
            print("Timeout waiting for the window.")
            return None
        time.sleep(1)


def capture_window(window):
    x, y, w, h = window.left, window.top, window.width, window.height
    return pyautogui.screenshot(region=(x, y, w, h))


def process_image(image, reference_color, key_positions):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    detected_keys = []
    for key, pos in key_positions.items():
        pixel_color = img[pos[1], pos[0]]
        if np.allclose(pixel_color, reference_color, atol=10):
            detected_keys.append(key)
    return detected_keys


def press_keys(keys):
    for key in keys:
        if key == 'SPACE':  # Special handling for the space key
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        elif len(key) == 1 and key.isalpha():  # Normal letter keys
            key = key.lower()  # Ensure lowercase
            keyboard.press(key)
            keyboard.release(key)
        else:  # Handle numeric and other keys normally
            keyboard.press(key)
            keyboard.release(key)



# Define the reference color (BGR format)
reference_color = (255, 255, 0)  # Cyan in BGR

# Key positions for the Spanish layout
key_positions = {
    '1': (65, 36), '2': (102, 36), '3': (136, 36), '4': (174, 36), '5': (210, 36),
    '6': (255, 37), '7': (289, 40), '8': (325, 39), '9': (359, 40), '0': (397, 42),
    'Q': (83, 82), 'W': (118, 82), 'E': (154, 82), 'R': (192, 82), 'T': (227, 82),
    'Y': (271, 82), 'U': (310, 82), 'I': (339, 82), 'O': (379, 82), 'P': (415, 82),
    'A': (95, 117), 'S': (134, 117), 'D': (167, 117), 'F': (201, 117), 'G': (239, 117),
    'H': (282, 117), 'J': (316, 117), 'K': (355, 117), 'L': (391, 117), 'Ñ': (427, 117),
    'Z': (116, 153), 'X': (152, 153), 'C': (188, 153), 'V': (223, 153), 'B': (257, 153),
    'N': (304, 153), 'M': (338, 153), 'SPACE': (276, 185)
}


def main():
    window = wait_and_focus_window("Teclado")
    if window:
        while True:
            img = capture_window(window)
            highlighted_keys = process_image(
                img, reference_color, key_positions)
            if highlighted_keys:
                press_keys(highlighted_keys)
            time.sleep(0.5)  # Adjust the delay as needed
    else:
        print("Failed to find the window.")


if __name__ == '__main__':
    main()
