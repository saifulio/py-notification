import time
from pynput import mouse, keyboard
from threading import Timer
from playsound import playsound  # Import for playing sound
from notifiers import get_notifier

# Variables
inactivity_time = 1 * 10  # 9 minutes
activity_detected = False
custom_sound_path = "notification_sound.wav"  # Path to your custom sound file

# Initialize the notifier
notifier = get_notifier('toast')  # 'toast' works for Windows notifications, and it should also work on macOS

# This function will notify user about inactivity
def notify_user():
    try:
        # Send a system notification
        notifier.notify(
            title="Inactivity Alert",
            message="It's been 9 minutes without activity! Please move the mouse or press a key."
        )
    except Exception as e:
        print(f"Failed to send notification: {e}")

    # Play custom sound
    playsound(custom_sound_path)

# Callback function for mouse and keyboard listeners
def on_activity(*args):
    global activity_detected
    activity_detected = True

# Listener classes for mouse and keyboard
mouse_listener = mouse.Listener(on_move=on_activity, on_click=on_activity, on_scroll=on_activity)
keyboard_listener = keyboard.Listener(on_press=on_activity)

# Function to monitor activity
def monitor_activity():
    global activity_detected
    while True:
        activity_detected = False
        time.sleep(inactivity_time)
        
        if not activity_detected:
            notify_user()

# Start the listeners
mouse_listener.start()
keyboard_listener.start()

# Start monitoring in the main thread
monitor_activity()
