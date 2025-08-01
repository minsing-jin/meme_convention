from meme_convention.setting.meme_adder import MemeAdder
from meme_convention.setting.music_player import MusicPlayer
from meme_convention.setting.setting_configuration import SystemSettingsModel

from tkinter import ttk, messagebox
from pathlib import Path
import tkinter as tk
import json
import threading


class SettingsManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.settings = self.load_settings()

    def load_settings(self) -> SystemSettingsModel:
        """Load settings from file or create default if not exists"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                return SystemSettingsModel(**data)
            except Exception as e:
                print(f"Error loading settings: {e}. Using defaults.")
                return SystemSettingsModel()
        else:
            return SystemSettingsModel()

    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.settings.model_dump(), f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def update_setting(self, key: str, value):
        """Update a specific setting and save"""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            self.save_settings()
        else:
            raise ValueError(f"Unknown setting: {key}")

    def get_setting(self, key: str):
        """Get a specific setting value"""
        return getattr(self.settings, key, None)


class SystemSettingsGUI(tk.Toplevel):
    def __init__(self, meme_contexts, external_settings_manager=None):
        super().__init__()
        self.title("System Settings")
        self.geometry("700x400")

        # Use external settings manager if provided, otherwise create new one
        if external_settings_manager:
            self.settings_manager = external_settings_manager
        else:
            self.settings_manager = SettingsManager()

        self.meme_adder = MemeAdder(meme_contexts)
        self.music_player = MusicPlayer()

        # Create Tkinter variables linked to settings
        self.keyboard_recording = tk.BooleanVar(value=self.settings_manager.get_setting('keyboard_recording'))
        self.music_chk_var = tk.BooleanVar(value=self.settings_manager.get_setting('music_enabled'))

        # Setup GUI components
        self.setup_ui()

        # Load current settings into UI
        self.load_settings_to_ui()

    def setup_ui(self):
        # Left listbox for options
        self.option_list = tk.Listbox(self, exportselection=False)
        self.option_list.insert(0, "Meme Adder")
        self.option_list.insert(1, "Music On/Off")
        self.option_list.insert(2, "Keyboard Typing Record")
        self.option_list.insert(3, "User Information Setting")
        self.option_list.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.option_list.bind('<<ListboxSelect>>', self.on_option_select)

        # Right frame to host setting widgets
        self.right_frame = ttk.Frame(self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.current_widgets = []

        # User info fields - now linked to settings
        self.user_info_vars = {}
        user_info = self.settings_manager.get_setting('user_info')
        for key, value in user_info.items():
            self.user_info_vars[key] = tk.StringVar(value=value)

        # Select first option by default
        self.option_list.selection_set(0)
        self.on_option_select()

    def load_settings_to_ui(self):
        """Load settings from the model into UI components"""
        # Update music player state
        if self.settings_manager.get_setting('music_enabled'):
            self.music_player.play_random_music()

        # Update keyboard recording state
        if self.settings_manager.get_setting('keyboard_recording'):
            self.start_keyboard_recording()

    def on_option_select(self, event=None):
        self.clear_right_frame()
        selected_indices = self.option_list.curselection()
        if not selected_indices:
            return
        selection = self.option_list.get(selected_indices[0])

        if selection == "Meme Adder":
            btn = ttk.Button(self.right_frame, text="Open Meme Adder Window",
                             command=self.meme_adder.show_meme_adder_window)
            btn.pack(pady=20)
            self.current_widgets.append(btn)

        elif selection == "Music On/Off":
            chk = ttk.Checkbutton(self.right_frame, text="Enable Music Playback",
                                  command=self.toggle_music,
                                  variable=self.music_chk_var)
            chk.pack(anchor="w", pady=20)
            self.current_widgets.append(chk)

        elif selection == "Keyboard Typing Record":
            chk = ttk.Checkbutton(self.right_frame, text="Enable Keyboard Typing Recording",
                                  variable=self.keyboard_recording,
                                  command=self.toggle_keyboard_recording)
            chk.pack(anchor="w", pady=20)
            self.current_widgets.append(chk)

            info_label = ttk.Label(self.right_frame, text="(Recording logic not implemented, placeholder)")
            info_label.pack(pady=5)
            self.current_widgets.append(info_label)

        elif selection == "User Information Setting":
            for key, var in self.user_info_vars.items():
                frm = ttk.Frame(self.right_frame)
                lbl = ttk.Label(frm, text=f"{key}: ", width=15)
                entry = ttk.Entry(frm, textvariable=var, width=30)
                lbl.pack(side="left")
                entry.pack(side="left", fill="x", expand=True)
                frm.pack(fill="x", pady=5)
                self.current_widgets.extend([frm, lbl, entry])

            save_btn = ttk.Button(self.right_frame, text="Save Info", command=self.save_user_info)
            save_btn.pack(pady=20)
            self.current_widgets.append(save_btn)

    def toggle_music(self):
        """Toggle music and save setting"""
        enabled = self.music_chk_var.get()
        self.settings_manager.update_setting('music_enabled', enabled)

        if enabled:
            started = self.music_player.play_random_music()
            if not started:
                messagebox.showwarning("Music", "No music files found or error playing music.")
                self.music_chk_var.set(False)
                self.settings_manager.update_setting('music_enabled', False)
        else:
            self.music_player.stop_music()

    def toggle_keyboard_recording(self):
        """Toggle keyboard recording and save setting"""
        enabled = self.keyboard_recording.get()
        self.settings_manager.update_setting('keyboard_recording', enabled)

        if enabled:
            self.start_keyboard_recording()
        else:
            self.stop_keyboard_recording()

    def start_keyboard_recording(self):
        print("Keyboard recording started...")
        # Implement your keyboard recording start logic here

    def stop_keyboard_recording(self):
        print("Keyboard recording stopped...")
        # Implement your stop logic here

    def save_user_info(self):
        """Save user information to settings"""
        info = {k: v.get() for k, v in self.user_info_vars.items()}
        self.settings_manager.update_setting('user_info', info)
        messagebox.showinfo("Information", "User info saved successfully.")

    def get_settings_manager(self):
        """Provide access to settings manager"""
        return self.settings_manager

    def clear_right_frame(self):
        for widget in self.current_widgets:
            widget.destroy()
        self.current_widgets.clear()

    def run(self):
        self.deiconify()
        self.lift()
        self.focus_force()
