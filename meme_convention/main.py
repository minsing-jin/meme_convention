import threading
import os, sys
import yaml
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from meme_convention.setting.hotkey import MainThreadExecutor
from meme_convention.autocomplete.autocomplete import AutoComplete, CONTEXT_CATEGORY_PATH
from meme_convention.db.local.local import LocalDB
from meme_convention.setting.meme_adder import MemeAdder
from meme_convention.recommendar.text_recorder import TypingRecorder

executor = MainThreadExecutor()
typing_recorder = TypingRecorder()
load_dotenv()

meme_adder_instance = None
keyboard_listener = None
config_file_path = 'setting_config.yaml'


def initialize_settings_config():
    if not os.path.exists(config_file_path):
        config_data = {
            'music_enabled': False,
            'keyboard_recording': False,
            'allow_screenshot': False,
            'context_category': [],
            'user_info': {'Age': '', 'Interest': '', 'Country': '', 'Location': '', 'Job': ''},
            'hot_key': '<ctrl>+<shift>+a'
        }
        with open(config_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
        print(f"Created configuration file: {config_file_path}")
    return config_file_path


def load_settings():
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
    try:
        with open(config_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(settings_data, f, default_flow_style=False, allow_unicode=True)
        print(f"Settings saved to {config_file_path}")
    except Exception as e:
        print(f"Failed to save settings: {e}")


def initialize_instances():
    global meme_adder_instance
    if meme_adder_instance is None:
        initialize_settings_config()
        meme_adder_instance = MemeAdder(contexts=[name for name in os.listdir(CONTEXT_CATEGORY_PATH)])


def run_autocomplete_main_thread():
    print("Running autocomplete on main thread...")
    try:
        local_db = LocalDB()
        autocomplete_instance = AutoComplete(db=local_db, typing_recorder=typing_recorder)
        result = autocomplete_instance.autocomplete()
        print(f"Autocomplete completed! Result: {result}")
    except Exception as e:
        print(f"Error in autocomplete: {e}")


def show_meme_adder_main_thread():
    print("Opening meme adder window...")
    try:
        initialize_instances()
        meme_adder_instance.show_meme_adder_window()
    except Exception as e:
        print(f"Error opening meme adder: {e}")


def run_autocomplete():
    print("Autocomplete hotkey detected! Scheduling autocomplete...")
    executor.add_task(run_autocomplete_main_thread)


def show_meme_adder():
    print("Meme adder hotkey detected! Opening meme adder...")
    executor.add_task(show_meme_adder_main_thread)


current_keys = set()

HOTKEYS = {}


def parse_hotkey(hotkey_str):
    """'<ctrl>+<shift>+a' 형식의 문자열을 pynput 키 객체의 집합으로 변환"""
    parts = hotkey_str.lower().replace(' ', '').split('+')
    keys = set()
    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            key_name = part[1:-1]
            if key_name.startswith('cmd'): key_name = 'cmd_l'  # macOS 호환성
            try:
                keys.add(getattr(Key, key_name))
            except AttributeError:
                print(f"Warning: Unknown special key '{key_name}' in hotkey '{hotkey_str}'")
        elif len(part) == 1:
            keys.add(KeyCode(char=part))
    return frozenset(keys)  # 변경 불가능한 set으로 반환


def update_hotkeys():
    """설정 파일에서 단축키를 읽어와 HOTKEYS 딕셔너리를 업데이트"""
    global HOTKEYS
    current_settings = load_settings()
    settings_hotkey_str = current_settings.get('hot_key', '<ctrl>+<shift>+a')

    # 설정 파일의 단축키
    settings_hotkey = parse_hotkey(settings_hotkey_str)

    # 고정 단축키
    autocomplete_hotkey_ctrl = parse_hotkey('<ctrl>+<shift>+m')
    autocomplete_hotkey_cmd = parse_hotkey('<cmd>+<shift>+m')

    HOTKEYS = {
        settings_hotkey: show_meme_adder,
        parse_hotkey('<cmd>+<shift>+a'): show_meme_adder,  # macOS용 대체
        autocomplete_hotkey_ctrl: run_autocomplete,
        autocomplete_hotkey_cmd: run_autocomplete,
    }
    print(f"Hotkeys updated. Meme Adder: {settings_hotkey_str}, Autocomplete: <ctrl/cmd>+<shift>+m")


def on_press(key):
    """키가 눌렸을 때 호출되는 함수"""
    # 1. 단축키 확인
    # frozenset은 순서가 없으므로 frozenset(current_keys)으로 비교하면 안됨
    # frozenset을 포함하는지 확인해야 함
    for hotkey, function in HOTKEYS.items():
        if key in hotkey and hotkey.issubset(current_keys.union({key})):
            function()
    current_keys.add(key)

    if key in [Key.f12, Key.f1, Key.f2, Key.f11,
               Key.media_volume_up, Key.media_volume_down, Key.media_volume_mute,
               Key.ctrl, Key.ctrl_l, Key.ctrl_r, Key.shift, Key.shift_l, Key.shift_r,
               Key.alt, Key.alt_l, Key.alt_r, Key.cmd, Key.cmd_l, Key.cmd_r]:
        return

    try:
        current_settings = load_settings()
        if not current_settings.get('keyboard_recording', False):
            return

        if hasattr(key, 'char') and key.char is not None:
            typing_recorder.record(key.char)
        else:
            special_key_map = {
                Key.space: ' ',
                Key.enter: '\n',
                Key.tab: '\t',
            }
            if key in special_key_map:
                typing_recorder.record(special_key_map[key])
            elif key == Key.backspace:
                typing_recorder.backspace()
    except Exception as e:
        print(f"Error in on_press logging: {e}")  # 디버깅을 위해 에러 출력


def on_release(key):
    """키에서 손을 뗐을 때 호출되는 함수"""
    try:
        current_keys.remove(key)
    except KeyError:
        pass


def start_keyboard_listener():
    """키보드 리스너를 시작하거나 재시작하는 통합 함수"""
    global keyboard_listener

    # 기존 리스너가 있다면 중지
    if keyboard_listener:
        try:
            keyboard_listener.stop()
            keyboard_listener.join(timeout=1.0)
            if keyboard_listener.is_alive():
                print("Warning: Keyboard listener did not stop gracefully.")
        except Exception as e:
            print(f"Error stopping keyboard listener: {e}")
        finally:
            keyboard_listener = None

    print("Starting unified keyboard listener...")
    update_hotkeys()  # 리스너 시작 전 최신 단축키 정보 로드

    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()


def monitor_settings_changes():
    last_modified = 0

    def check_file_changes():
        nonlocal last_modified
        try:
            if os.path.exists(config_file_path):
                current_modified = os.path.getmtime(config_file_path)
                if current_modified != last_modified:
                    last_modified = current_modified
                    print("Settings file changed, restarting keyboard listener to apply changes...")
                    # 리스너 재시작 시 단축키 설정도 다시 로드됨
                    start_keyboard_listener()
        except Exception as e:
            print(f"Error monitoring settings: {e}")

    def monitor_worker():
        import time
        while True:
            check_file_changes()
            time.sleep(2)

    monitor_thread = threading.Thread(target=monitor_worker, daemon=True)
    monitor_thread.start()


def main():
    print("🚀 Starting program with unified listener...")

    initialize_settings_config()

    # 통합 리스너 시작 (이 안에서 hotkey 설정도 로드합니다)
    start_keyboard_listener()

    # 설정 파일 변경 감지 시작
    monitor_settings_changes()

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
