import time
from pynput import mouse, keyboard
from threading import Thread
from playsound import playsound
from notifiers import get_notifier

# Variables
inactivity_time = 1 * 15  # 9 minutes
subsequent_alert_interval = 10  # 1 minute for subsequent alerts
activity_detected = False
custom_sound_path = "notification_sound.wav"  # Initial custom sound file
repeat_sound_path = "repeat_alert.wav"  # Sound file for subsequent alerts

# Initialize the notifier
notifier = get_notifier('toast')  # Cross-platform notifier

# This function will notify the user about inactivity
def notify_user():
    # Send a system notification
    try:
        notifier.notify(
            title="Inactivity Alert",
            message="It's been 9 minutes without activity! Please move the mouse or press a key."
        )
    except Exception as e:
        print(f"Failed to send notification: {e}")

    # Play custom sound
    playsound(custom_sound_path)

# This function will play the repeated alert sound every minute if there's no activity
def play_repeat_sound():
    while not activity_detected:
        playsound(repeat_sound_path)
        time.sleep(subsequent_alert_interval)

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
        # Reset the activity flag
        activity_detected = False

        # Wait for the initial inactivity time (9 minutes)
        start_time = time.time()
        while time.time() - start_time < inactivity_time:
            if activity_detected:
                break
            time.sleep(1)

        # If activity is detected, restart the loop
        if activity_detected:
            continue

        # If no activity detected, notify the user and start repeated alerts
        notify_user()

        # Start playing the repeat alert every minute until activity is detected
        while not activity_detected:
            playsound(repeat_sound_path)
            for _ in range(subsequent_alert_interval):
                if activity_detected:
                    break
                time.sleep(1)

# Start the listeners in separate threads
mouse_listener.start()
keyboard_listener.start()

# Start monitoring in the main thread
monitor_activity()
