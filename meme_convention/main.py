from pynput import keyboard
import threading
from dotenv import load_dotenv
from utils.hotkey import MainThreadExecutor
from meme_convention.meme_feature.autocomplete import AutoComplete
from meme_convention.db.postgresql.postgresql import POSTGRESQL
from meme_convention.db.local.local import LocalDB
from meme_convention.db.get_from_web.tenor import TenorMemeProvider
from meme_convention.db.get_from_web.giphy import GiphyMemeProvider

# Create global executor instance
executor = MainThreadExecutor()
load_dotenv()


def run_autocomplete_main_thread():
    """Function to run autocomplete on main thread"""
    print("Running autocomplete on main thread...")
    try:
        db = POSTGRESQL()
        local_db = LocalDB()
        tenor_meme_provider = TenorMemeProvider()
        giphiy_meme_provider = GiphyMemeProvider()

        autocomplete = AutoComplete(db=local_db,analysis_model=None, text=None, page_image=None)
        result = autocomplete.autocomplete(["pr", "issue", "bug", "feature", "code review"])
        print(f"Autocomplete completed! Result: {result}")
    except Exception as e:
        print(f"Error: {e}")


def run_autocomplete():
    """Function to run when hotkey is pressed"""
    print("Hotkey detected! Scheduling autocomplete...")
    executor.add_task(run_autocomplete_main_thread)


def start_hotkey_listener_async():
    """Start hotkey listener in background thread"""

    def hotkey_worker():
        print("Hotkey listener started. Press Ctrl+Shift+A to run autocomplete.")
        with keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+a': run_autocomplete,
            '<cmd>+<shift>+a': run_autocomplete
        }) as hotkeys:
            hotkeys.join()

    hotkey_thread = threading.Thread(target=hotkey_worker)
    hotkey_thread.daemon = True
    hotkey_thread.start()
    return hotkey_thread

def main():
    """Main function that keeps the main thread active"""
    print("🚀 Starting hotkey program...")

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
