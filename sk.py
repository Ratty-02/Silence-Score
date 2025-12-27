import time
import csv
import math
import os
from datetime import datetime
from pynput import keyboard, mouse
import psutil
import win32gui
import win32process

key_count = 0
mouse_distance = 0
last_mouse_position = None


desktop = os.path.join(os.path.expanduser("~"), "Desktop")
filename = f"activity_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
log_path = os.path.join(desktop, filename)

def on_press(key):
    global key_count
    key_count += 1

def on_move(x, y):
    global mouse_distance, last_mouse_position
    if last_mouse_position:
        dx = x - last_mouse_position[0]
        dy = y - last_mouse_position[1]
        mouse_distance += math.sqrt(dx**2 + dy**2)  
    last_mouse_position = (x, y)

def get_active_app():
    """Return the active window's process name and title."""
    try:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd == 0:
            return "no window"
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        process_name = process.name()
        window_title = win32gui.GetWindowText(hwnd)
        if not window_title.strip():
            window_title = "no title"
        return f"{process_name} ({window_title})"
    except Exception as e:
        return f"error: {e}"

def classify(score):
    if score >= 70:
        return "Deep Work"
    elif score >= 40:
        return "Shallow Work"
    else:
        return "Fake Productivity"

def start_logging(interval=5):
    global key_count, mouse_distance

    os.makedirs(desktop, exist_ok=True)

    with open(log_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "keys", "mouse", "app", "keys_per_sec", "classification"])

        while True:
            kps = key_count / interval
       
            score = min((kps * 20) + (mouse_distance / 100), 100)
            label = classify(score)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                key_count,
                round(mouse_distance, 2),
                get_active_app(),
                round(kps, 2),
                label
            ])
            print("Logged data to:", log_path)
            key_count = 0
            mouse_distance = 0
            time.sleep(interval)

if __name__ == "__main__":
    keyboard.Listener(on_press=on_press).start()
    mouse.Listener(on_move=on_move).start()
    start_logging()
import pandas as pd
import matplotlib.pyplot as plt


def extract_features(path):
    # Load CSV into DataFrame
    return pd.read_csv(path)

def calculate_silence_score(row):
    
    focus = min(row["keys"] * 5, 40)
    consistency = 30 if "Search" not in str(row["app"]) else 10
    interaction = min(row["keys_per_sec"] * 10, 30)
    return round(min(focus + consistency + interaction, 100), 2)


def classify(score):
    if score >= 70:
        return "Deep Work"
    elif score >= 40:
        return "Shallow Work"
    else:
        return "Fake Productivity"


df = extract_features("../data/activity_log.csv")


df["silence_score"] = df.apply(calculate_silence_score, axis=1)
df["label"] = df["silence_score"].apply(classify)


plt.figure(figsize=(12,6))
plt.plot(df["silence_score"], marker="o", linestyle="-", color="black", label="Silence Score")


for i, (score, label) in enumerate(zip(df["silence_score"], df["label"])):
    if label == "Deep Work":
        plt.scatter(i, score, color="green", s=50, label="Deep Work" if i==0 else "")
    elif label == "Shallow Work":
        plt.scatter(i, score, color="orange", s=50, label="Shallow Work" if i==0 else "")
    else:
        plt.scatter(i, score, color="red", s=50, label="Fake Productivity" if i==0 else "")

plt.title("Silence Score Over Time")
plt.xlabel("Time Window (row index)")
plt.ylabel("Score")
plt.legend()
plt.grid(True)
plt.show()


print(df[["silence_score", "label"]].tail())
