# Check is this safe privacy-wise
from datetime import datetime, timedelta
import threading
from collections import deque
from pynput import keyboard


# TODO: 영어인지 한국어인지 구별, When typing recoder start to record?
class TypingRecorder:
    def __init__(self, maxlen=500):
        self.typed = deque(maxlen=maxlen)  # automatically discards oldest
        self.lock = threading.Lock()

    def backspace(self):
        with self.lock:
            if self.typed:
                self.typed.pop()

    def record(self, char):
        with self.lock:
            now = datetime.now()
            self.typed.append((char, now))
            # Prune old entries beyond 20s
            cutoff = now - timedelta(seconds=80)
            while self.typed and self.typed[0][1] < cutoff:
                self.typed.popleft()

    def get_last(self, seconds=15):
        with self.lock:
            cutoff = datetime.now() - timedelta(seconds=seconds)
            return ''.join(c for c, t in self.typed if t >= cutoff)
