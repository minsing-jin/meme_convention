# Check is this safe privacy-wise
from datetime import datetime, timedelta
import threading
from collections import deque
from pynput import keyboard

class TypingRecorder:
    def __init__(self, maxlen=500):
        self.typed = deque(maxlen=maxlen)  # automatically discards oldest
        self.lock = threading.Lock()

    def record(self, char):
        with self.lock:
            now = datetime.now()
            self.typed.append((char, now))
            # Prune old entries beyond 20s
            cutoff = now - timedelta(seconds=20)
            while self.typed and self.typed[0][1] < cutoff:
                self.typed.popleft()

    def get_last(self, seconds=15):
        with self.lock:
            cutoff = datetime.now() - timedelta(seconds=seconds)
            return ''.join(c for c, t in self.typed if t >= cutoff)


typing_recorder = TypingRecorder()

def on_press(key):
    try:
        # Only record printable characters
        if hasattr(key, 'char') and key.char is not None:
            typing_recorder.record(key.char)
    except Exception:
        pass  # Ignore any errors such as special keys without char

def on_activate():
    recent_text = typing_recorder.get_last(15)
    print(f"\n--- Last 15 seconds of typing ---\n{recent_text}\n-------------------------------")

if __name__ == "__main__":
    # Set the hotkey Ctrl+Shift+M to print recent typing
    hotkey = keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+m': on_activate
    })

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    print("Start typing. Press Ctrl+Shift+M to display text typed in last 15 seconds. Press Ctrl+C to quit.")

    hotkey.start()
    hotkey.join()