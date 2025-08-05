from pynput import keyboard
from pynput.keyboard import Key
import threading
from dotenv import load_dotenv
import os, sys
import yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from meme_convention.setting.hotkey import MainThreadExecutor
from meme_convention.autocomplete.autocomplete import AutoComplete, CONTEXT_CATEGORY_PATH
from meme_convention.db.local.local import LocalDB
from meme_convention.setting.system_setting_gui import SystemSettingsGUI
from meme_convention.recommendar.text_recorder import TypingRecorder
from utils.utils import load_yaml_file

# Create global executor instance
executor = MainThreadExecutor()
typing_recorder = TypingRecorder()
load_dotenv()

# Global instances
system_setting_gui_instance = None
keyboard_listener = None
config_file_path = 'setting_config.yaml'


def initialize_settings_config():
    """Initialize configuration file if it doesn't exist"""
    if not os.path.exists(config_file_path):
        config_data = {
            'music_enabled': False,
            'keyboard_recording': False,
            'allow_screenshot': False,
            'context_category': [],
            'user_info': {
                'Age': '',
                'Interest': '',
                'Country': '',
                'Location': '',
                'Job': ''
            },
            'hot_key': '<ctrl>+<shift>+a'
        }

        with open(config_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
        print(f"Created configuration file: {config_file_path}")

    return config_file_path


def load_settings():
    """Load settings from YAML file"""
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        print(f"[YAML ERROR] Failed to parse settings: {e}")
        return {}
    except Exception as e:
        print(f"[LOAD ERROR] Failed to load settings: {e}")
        return {}


def save_settings(settings_data):
    """Save settings to YAML file"""
    try:
        with open(config_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(settings_data, f, default_flow_style=False, allow_unicode=True)
        print(f"Settings saved to {config_file_path}")
    except Exception as e:
        print(f"Failed to save settings: {e}")


def initialize_instances():
    """Initialize SystemSettingsGUI instance"""
    global system_setting_gui_instance
    if system_setting_gui_instance is None:
        # Ensure configuration file exists
        initialize_settings_config()

        system_setting_gui_instance = SystemSettingsGUI(
            yaml_file_path=config_file_path,
            contexts=[name for name in os.listdir(CONTEXT_CATEGORY_PATH)]
        )


def run_autocomplete_main_thread():
    """Function to run autocomplete on main thread"""
    print("Running autocomplete on main thread...")
    try:
        config_data = load_settings()

        local_db = LocalDB()
        autocomplete_instance = AutoComplete(
            db=local_db,
            typing_recorder=typing_recorder,
            config_data=config_data
        )

        result = autocomplete_instance.autocomplete()
        print(f"Autocomplete completed! Result: {result}")
    except Exception as e:
        print(f"Error in autocomplete: {e}")


def show_system_settings_main_thread():
    """Function to show system settings on main thread"""
    print("Opening system settings window...")
    try:
        initialize_instances()
        system_setting_gui_instance.run()
    except Exception as e:
        print(f"Error opening system settings: {e}")


def run_autocomplete():
    """Function to run when autocomplete hotkey is pressed"""
    print("Autocomplete hotkey detected! Scheduling autocomplete...")
    executor.add_task(run_autocomplete_main_thread)


def show_system_settings():
    """Function to run when system settings hotkey is pressed"""
    print("System settings hotkey detected! Opening system settings...")
    executor.add_task(show_system_settings_main_thread)


def start_hotkey_listener_async():
    """Start hotkey listener in background thread"""

    def hotkey_worker():
        # Load current settings
        current_settings = load_settings()
        settings_hotkey = current_settings.get('hot_key', '<ctrl>+<shift>+a')

        # Validate hotkey before using it
        if not settings_hotkey or settings_hotkey.strip() == "":
            print("Warning: No hotkey configured, using default")
            settings_hotkey = '<ctrl>+<shift>+a'

        print(f"Using settings hotkey: {settings_hotkey}")

        try:
            with keyboard.GlobalHotKeys({
                settings_hotkey: show_system_settings,
                '<cmd>+<shift>+a': show_system_settings,
                '<ctrl>+<shift>+m': run_autocomplete,
                '<cmd>+<shift>+m': run_autocomplete
            }) as hotkeys:
                hotkeys.join()
        except ValueError as e:
            print(f"Invalid hotkey format: {e}")
            print(f"Problematic hotkey: {settings_hotkey}")
            # Use fallback hotkeys only
            with keyboard.GlobalHotKeys({
                '<ctrl>+<shift>+a': show_system_settings,
                '<cmd>+<shift>+a': show_system_settings,
                '<ctrl>+<shift>+m': run_autocomplete,
                '<cmd>+<shift>+m': run_autocomplete
            }) as hotkeys:
                hotkeys.join()

    hotkey_thread = threading.Thread(target=hotkey_worker, daemon=True)
    hotkey_thread.start()
    return hotkey_thread


def on_press(key):
    """Handle key press events for typing recording"""
    try:
        current_settings = load_settings()

        # Only record if keyboard recording is enabled
        if not current_settings.get('keyboard_recording', False):
            return

        if hasattr(key, 'char') and key.char is not None:
            typing_recorder.record(key.char)
        else:
            # Handle special keys explicitly
            if key == Key.space:
                typing_recorder.record(' ')
            elif key == Key.enter:
                typing_recorder.record('\n')
            elif key == Key.tab:
                typing_recorder.record('\t')
            elif key == Key.backspace:
                typing_recorder.backspace()
    except Exception as e:
        # Silent fail for performance
        pass


def start_keyboard_listener():
    """Start keyboard listener if recording is enabled"""
    global keyboard_listener

    current_settings = load_settings()

    # Stop existing listener if running
    if keyboard_listener:
        try:
            keyboard_listener.stop()
            keyboard_listener.join(timeout=1.0)  # 타임아웃 추가
            if keyboard_listener.is_alive():
                print("Warning: Keyboard listener did not stop gracefully.")
        except Exception as e:
            print(f"Error stopping keyboard listener: {e}")
        finally:
            keyboard_listener = None

    # Start new listener if keyboard recording is enabled
    if current_settings.get('keyboard_recording', False):
        print("Starting keyboard listener (enabled in settings)")
        keyboard_listener = keyboard.Listener(on_press=on_press)
        keyboard_listener.start()
    else:
        print("Keyboard recording disabled in settings")


def restart_keyboard_listener():
    """Restart keyboard listener with current settings"""
    start_keyboard_listener()


def monitor_settings_changes():
    """Monitor settings file for changes and restart services if needed"""
    last_modified = 0

    def check_file_changes():
        nonlocal last_modified
        try:
            if os.path.exists(config_file_path):
                current_modified = os.path.getmtime(config_file_path)
                if current_modified != last_modified:
                    last_modified = current_modified
                    print("Settings file changed, restarting keyboard listener...")
                    start_keyboard_listener()
        except Exception as e:
            print(f"Error monitoring settings: {e}")

    # Check for changes every 2 seconds
    def monitor_worker():
        import time
        while True:
            check_file_changes()
            time.sleep(2)

    monitor_thread = threading.Thread(target=monitor_worker, daemon=True)
    monitor_thread.start()


def main():
    print("🚀 Starting hotkey program...")

    # Initialize configuration at startup
    initialize_settings_config()

    # Load current settings
    current_settings = load_settings()
    hotkey_combo = current_settings.get('hot_key', '<ctrl>+<shift>+a')
    print(f"Using hotkey: {hotkey_combo}")

    # Start keyboard listener based on current settings
    start_keyboard_listener()

    # Start settings file monitoring
    monitor_settings_changes()

    # Start hotkey listener in background
    start_hotkey_listener_async()

    try:
        print("System ready! Press configured hotkeys to interact.")
        executor.run_main_loop()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
        executor.running = False
        if keyboard_listener:
            keyboard_listener.stop()


if __name__ == "__main__":
    main()
