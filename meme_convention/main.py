from pynput import keyboard
from pynput.keyboard import Key
import threading
from dotenv import load_dotenv
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from meme_convention.setting.hotkey import MainThreadExecutor
from meme_convention.autocomplete.autocomplete import AutoComplete
from meme_convention.db.local.local import LocalDB
from meme_convention.setting.meme_adder import MemeAdder  # Import the new meme adder
from meme_convention.recommendar.text_recorder import TypingRecorder

# from meme_convention.db.postgresql.postgresql import POSTGRESQL
# from meme_convention.db.get_from_web.tenor import TenorMemeProvider
# from meme_convention.db.get_from_web.giphy import GiphyMemeProvider

# Create global executor instance
executor = MainThreadExecutor()
typing_recorder = TypingRecorder()
load_dotenv()

# TODO: We have to bring context categories at specific directory and read context folders names
# TODO: Convert data type to dictionary {context: description}
CONTEXTS = ["pr", "issue", "bug", "feature", "code review", "refactoring"]

def run_autocomplete_main_thread():
    """Function to run autocomplete on main thread"""
    print("Running autocomplete on main thread...")
    try:
        local_db = LocalDB()
        # tenor_meme_provider = TenorMemeProvider()
        # giphiy_meme_provider = GiphyMemeProvider()
        # db = POSTGRESQL()

        autocomplete = AutoComplete(db=local_db, typing_recorder=typing_recorder)
        result = autocomplete.autocomplete(CONTEXTS)
        print(f"Autocomplete completed! Result: {result}")
    except Exception as e:
        print(f"Error: {e}")


def show_meme_adder_main_thread():
    """Function to show meme adder on main thread"""
    print("Opening meme adder window...")
    meme_adder = MemeAdder(CONTEXTS)
    try:
        meme_adder.show_meme_adder_window()
    except Exception as e:
        print(f"Error opening meme adder: {e}")


def run_autocomplete():
    """Function to run when autocomplete hotkey is pressed"""
    print("Autocomplete hotkey detected! Scheduling autocomplete...")
    executor.add_task(run_autocomplete_main_thread)


def show_meme_adder():
    """Function to run when meme adder hotkey is pressed"""
    print("Meme adder hotkey detected! Opening meme adder...")
    executor.add_task(show_meme_adder_main_thread)


def start_hotkey_listener_async():
    """Start hotkey listener in background thread"""

    def hotkey_worker():
        print("Hotkey listener started.")
        print("Press Ctrl+Shift+A to run autocomplete.")
        print("Press Ctrl+Shift+M to open meme adder.")

        with keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+a': show_meme_adder,
            '<cmd>+<shift>+a': show_meme_adder,
            '<ctrl>+<shift>+m': run_autocomplete,
            '<cmd>+<shift>+m': run_autocomplete
        }) as hotkeys:
            hotkeys.join()

    hotkey_thread = threading.Thread(target=hotkey_worker)
    hotkey_thread.daemon = True
    hotkey_thread.start()
    return hotkey_thread

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            typing_recorder.record(key.char)
        else:
            # Handle special keys explicitly
            if key == Key.space:
                typing_recorder.record(' ')
            elif key == Key.enter:
                # Record newline
                typing_recorder.record('\n')
            elif key == Key.tab:
                typing_recorder.record('\t')
            elif key == Key.backspace:
                # Remove the last character if present (simulate backspace)
                typing_recorder.backspace()
            # You can add more keys here if needed
    except Exception:
        pass

def main():
    print("🚀 Starting hotkey program...")

    # Start the keyboard listener to record typing
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Start hotkey listener in background
    start_hotkey_listener_async()

    # Run the main GUI loop
    try:
        executor.run_main_loop()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
        executor.running = False


if __name__ == "__main__":
    main()
