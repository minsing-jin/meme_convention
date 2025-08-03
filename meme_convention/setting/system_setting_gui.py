import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any
from .setting_configuration import SystemSettingsConfiguration, SystemSettingsModel
from meme_convention.setting.meme_adder import MemeAdder

# TODO: add music add feature
class SystemSettingsGUI:
    def __init__(self, settings_manager: SystemSettingsConfiguration = None):
        self.settings_manager = settings_manager or SystemSettingsConfiguration()
        self.root = None
        self.widgets = {}
        self.meme_adder = None  # Add this line

    def create_gui(self):
        """Create the main GUI window"""
        self.root = tk.Tk()
        self.root.title("System Settings")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.create_general_tab(notebook)
        self.create_user_info_tab(notebook)
        self.create_meme_contexts_tab(notebook)

        # Create buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='x', padx=10, pady=(0, 10))

        # Buttons
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right')
        ttk.Button(button_frame, text="Reset to Default", command=self.reset_to_default).pack(side='left')

        # Add Meme Adder button
        ttk.Button(button_frame, text="Open Meme Adder",
                   command=self.open_meme_adder).pack(side='left', padx=(10, 0))

        # Load current settings
        self.load_current_settings()

    def open_meme_adder(self):
        """Open the meme adder window with current contexts"""
        try:
            # Get current meme contexts from the listbox
            current_contexts = []
            for i in range(self.widgets['meme_contexts_listbox'].size()):
                current_contexts.append(self.widgets['meme_contexts_listbox'].get(i))

            if not current_contexts:
                messagebox.showwarning("No Contexts",
                                       "Please add some meme contexts first before opening the meme adder!")
                return

            # Create and show meme adder
            self.meme_adder = MemeAdder(current_contexts)
            self.meme_adder.show_meme_adder_window()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open meme adder: {str(e)}")

    def create_general_tab(self, notebook):
        """Create the general settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="General")

        # Music enabled
        self.widgets['music_enabled'] = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Enable Music Playback",
                        variable=self.widgets['music_enabled']).pack(anchor='w', pady=5)

        # Keyboard recording
        self.widgets['keyboard_recording'] = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Enable Keyboard Recording",
                        variable=self.widgets['keyboard_recording']).pack(anchor='w', pady=5)

        # Allow screenshot
        self.widgets['allow_screenshot'] = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Allow Screenshots",
                        variable=self.widgets['allow_screenshot']).pack(anchor='w', pady=5)

        # Hotkey setting
        hotkey_frame = ttk.LabelFrame(frame, text="Hotkey Settings", padding=10)
        hotkey_frame.pack(fill='x', pady=10)

        ttk.Label(hotkey_frame, text="System Settings Hotkey:").pack(anchor='w')
        self.widgets['hot_key'] = tk.StringVar()
        ttk.Entry(hotkey_frame, textvariable=self.widgets['hot_key'], width=30).pack(anchor='w', pady=5)

    def create_user_info_tab(self, notebook):
        """Create the user information tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="User Info")

        # Create scrollable frame
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # User info fields
        self.widgets['user_info'] = {}
        user_info_fields = ['Age', 'Interest', 'Country', 'Location', 'Job']

        for field in user_info_fields:
            field_frame = ttk.Frame(scrollable_frame)
            field_frame.pack(fill='x', pady=5)

            ttk.Label(field_frame, text=f"{field}:", width=15).pack(side='left')
            self.widgets['user_info'][field] = tk.StringVar()
            ttk.Entry(field_frame, textvariable=self.widgets['user_info'][field],
                      width=40).pack(side='left', fill='x', expand=True)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_meme_contexts_tab(self, notebook):
        """Create the meme contexts tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Meme Contexts")

        # Meme contexts listbox with scrollbar
        list_frame = ttk.LabelFrame(frame, text="Current Meme Contexts", padding=10)
        list_frame.pack(fill='both', expand=True, pady=5)

        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill='both', expand=True)

        self.widgets['meme_contexts_listbox'] = tk.Listbox(listbox_frame)
        scrollbar_meme = ttk.Scrollbar(listbox_frame, orient="vertical",
                                       command=self.widgets['meme_contexts_listbox'].yview)
        self.widgets['meme_contexts_listbox'].configure(yscrollcommand=scrollbar_meme.set)

        self.widgets['meme_contexts_listbox'].pack(side="left", fill="both", expand=True)
        scrollbar_meme.pack(side="right", fill="y")

        # Add/Remove buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', pady=(10, 0))

        # Entry for new context
        self.widgets['new_context'] = tk.StringVar()
        ttk.Entry(button_frame, textvariable=self.widgets['new_context'],
                  width=30).pack(side='left', fill='x', expand=True)

        ttk.Button(button_frame, text="Add", command=self.add_meme_context).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Remove Selected",
                   command=self.remove_meme_context).pack(side='right')

    def load_current_settings(self):
        """Load current settings from the configuration"""
        settings = self.settings_manager.get_settings()

        # Load general settings
        self.widgets['music_enabled'].set(settings.music_enabled)
        self.widgets['keyboard_recording'].set(settings.keyboard_recording)
        self.widgets['allow_screenshot'].set(settings.allow_screenshot)
        self.widgets['hot_key'].set(settings.hot_key)

        # Load user info
        for key, value in settings.user_info.items():
            if key in self.widgets['user_info']:
                self.widgets['user_info'][key].set(value)

        # Load meme contexts
        self.widgets['meme_contexts_listbox'].delete(0, tk.END)
        for context in settings.meme_contexts:
            self.widgets['meme_contexts_listbox'].insert(tk.END, context)

    def save_settings(self):
        """Save current settings to configuration"""
        try:
            # Collect general settings
            settings_data = {
                'music_enabled': self.widgets['music_enabled'].get(),
                'keyboard_recording': self.widgets['keyboard_recording'].get(),
                'allow_screenshot': self.widgets['allow_screenshot'].get(),
                'hot_key': self.widgets['hot_key'].get(),
            }

            # Collect user info
            user_info = {}
            for key, var in self.widgets['user_info'].items():
                user_info[key] = var.get()
            settings_data['user_info'] = user_info

            # Collect meme contexts
            meme_contexts = []
            for i in range(self.widgets['meme_contexts_listbox'].size()):
                meme_contexts.append(self.widgets['meme_contexts_listbox'].get(i))
            settings_data['meme_contexts'] = meme_contexts

            # Update settings
            if self.settings_manager.update_settings(**settings_data):
                messagebox.showinfo("Success", "Settings saved successfully!")
                self.root.destroy()
            else:
                messagebox.showerror("Error", "Failed to save settings!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def cancel(self):
        """Cancel and close the window"""
        self.root.destroy()

    def reset_to_default(self):
        """Reset all settings to default values"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all settings to default?"):
            default_settings = SystemSettingsModel()
            settings_data = default_settings.model_dump()

            if self.settings_manager.update_settings(**settings_data):
                self.load_current_settings()
                messagebox.showinfo("Success", "Settings reset to default!")
            else:
                messagebox.showerror("Error", "Failed to reset settings!")

    def add_meme_context(self):
        """Add a new meme context"""
        new_context = self.widgets['new_context'].get().strip()
        if new_context:
            # Check if context already exists
            existing_contexts = []
            for i in range(self.widgets['meme_contexts_listbox'].size()):
                existing_contexts.append(self.widgets['meme_contexts_listbox'].get(i))

            if new_context not in existing_contexts:
                self.widgets['meme_contexts_listbox'].insert(tk.END, new_context)
                self.widgets['new_context'].set("")  # Clear entry
            else:
                messagebox.showwarning("Duplicate", "This context already exists!")
        else:
            messagebox.showwarning("Empty Context", "Please enter a context name!")

    def remove_meme_context(self):
        """Remove selected meme context"""
        selection = self.widgets['meme_contexts_listbox'].curselection()
        if selection:
            self.widgets['meme_contexts_listbox'].delete(selection[0])
        else:
            messagebox.showwarning("No Selection", "Please select a context to remove!")

    def run(self):
        """Run the GUI"""
        self.create_gui()
